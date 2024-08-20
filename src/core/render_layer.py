from src.core.sprite import Sprite

from typing import Callable, Iterable
from enum import Enum
import pygame

class RenderLayer:
    def __init__(self, key: Callable[[Sprite], int] = None) -> None:
        self.key = key
        self.sprites: list[Sprite] = []
        self.bound_sprites: dict[Sprite, Sprite] = {}

    def update(self, dt: float) -> None:
        if self.key is not None:
            self.sprites.sort(key=self.key)

        for sprite in self.sprites:
            sprite.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        for sprite in self.sprites:
            self._draw_sprite(sprite, screen)

    def _draw_sprite(self, sprite: Sprite, screen: pygame.Surface) -> None:
        sprite.draw(screen)
        # Recursively draw bound sprites
        if sprite in self.bound_sprites:
            self._draw_sprite(self.bound_sprites[sprite], screen)
            self._draw_sprite(self.bound_sprites[sprite], screen)

    def add(self, sprite: Sprite) -> None:
        self.sprites.append(sprite)

    def remove(self, sprite: Sprite) -> None:
        try:
            self.sprites.remove(sprite)
        except ValueError:
            pass

    def bind(self, bottom: Sprite, top: Sprite) -> None:
        if top in self.bound_sprites:
            # Generate a trace of the cyclical binding
            stack = [current := top]
            while current in self.bound_sprites:
                stack.append(current := self.bound_sprites[current])
            trace = " -> ".join(map(str, stack))
            raise ValueError(f"Cyclical binding detected: \n{trace}")

        try:
            self.remove(top)
        except ValueError:
            # top either doesn't exist in the layer or has been removed
            # from being bound to another sprite
            pass
        self.bound_sprites[bottom] = top

    def unbind(self, bottom: Sprite) -> bool:
        if bottom in self.bound_sprites:
            del self.bound_sprites[bottom]
            return True
        return False

    def __len__(self) -> int:
        return len(self.sprites) + len(self.bound_sprites)

class FilteredRenderLayer(RenderLayer):
    def __init__(self, filter: Callable[[Sprite], bool]) -> None:
        super().__init__()
        self.filter = filter

    def update(self, dt: float) -> None:
        for sprite in filter(self.filter, self.sprites):
            sprite.update(dt)

class SelectiveRenderLayer(RenderLayer):
    def __init__(self, selector: Callable[[RenderLayer], Iterable[Sprite]]) -> None:
        super().__init__()
        self.selector = selector

    def update(self, dt: float) -> None:
        for sprite in self.selector(self):
            sprite.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        for sprite in self.selector(self):
            self._draw_sprite(sprite, screen)

class NoRenderLayer(RenderLayer):
    def __init__(self) -> None:
        super().__init__()

    def draw(self, screen: pygame.Surface) -> None:
        pass

class Layer(Enum):
    BLOB = NoRenderLayer
    INK = RenderLayer
    PIN = RenderLayer
    UI = RenderLayer
