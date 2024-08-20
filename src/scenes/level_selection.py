from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game

from src.sprites.button import Button
from src.scenes.level import levels
from src.core.glpg import Texture
from src.core.scene import Scene

from pygame.locals import SRCALPHA
import pygame

class LevelSelection(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__(game)

        surf = pygame.Surface(self.game.window.size, SRCALPHA)
        surf.fill((0, 0, 0, 255))
        self.background = Texture(self.game.window, surf)

        self.level_buttons = []
        for i, level in enumerate(levels):
            bt = Button(self, (400 + 800 * i, 400), str(i + 1), 140, lambda level=level: self.game.change_scene(level(self.game)))
            self.add(bt)
            self.level_buttons.append(bt)

        self.add(Button(self, (100, 400), "<", 40, self.scroll_left, scale=0.8))
        self.add(Button(self, (700, 400), ">", 40, self.scroll_right, scale=0.8))

    def update(self, dt: float) -> None:
        self.sprite_manager.update(dt)

    def scroll_left(self) -> None:
        if self.level_buttons[0].pos.x >= 400: return
        for button in self.level_buttons:
            button.pos.x += 800

    def scroll_right(self) -> None:
        if self.level_buttons[-1].pos.x <= 400: return
        for button in self.level_buttons:
            button.pos.x -= 800

    def draw(self, screen: pygame.Surface) -> None:
        self.game.texture.blit(self.background, (0, 0))
        self.sprite_manager.draw(screen)
