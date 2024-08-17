from src.core.sprite import Sprite

from typing import Callable
from enum import Enum, auto
import pygame

class Layer(Enum):
    BACKGROUND = auto()
    DEFAULT = auto()
    HUD = auto()

class RenderLayer:
    def __init__(self, key: Callable[[Sprite], int] = None) -> None:
        self.key = key
        self.sprites: list[Sprite] = []
        self.bounded_sprites: dict[Sprite, Sprite] = {}

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
        # Recursively draw bounded sprites
        if sprite in self.bounded_sprites:
            self._draw_sprite(self.bounded_sprites[sprite], screen)

    def add(self, sprite: Sprite) -> None:
        self.sprites.append(sprite)

    def remove(self, sprite: Sprite) -> None:
        self.sprites.remove(sprite)

    def bind(self, bottom: Sprite, top: Sprite) -> None:
        if top in self.bounded_sprites:
            # Generate a trace of the cyclical binding
            stack = [current := top]
            while current in self.bounded_sprites:
                stack.append(current := self.bounded_sprites[current])
            trace = " -> ".join(map(str, stack))
            raise ValueError(f"Cyclical binding detected: \n{trace}")

        try:
            self.remove(top)
        except ValueError:
            # top either doesn't exist in the layer or has been removed
            # from being bound to another sprite
            pass
        self.bounded_sprites[bottom] = top

    def __len__(self) -> int:
        return len(self.sprites) + len(self.bounded_sprites)
