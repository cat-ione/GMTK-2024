from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game

from src.core.glpg import Texture, Shader
from src.sprites.button import Button
from src.scenes.level import levels
from src.core.scene import Scene

from pygame.locals import SRCALPHA
import pygame

class MainMenu(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__(game)

        surf = pygame.Surface(self.game.window.size, SRCALPHA)
        surf.fill((0, 0, 0, 255))
        self.background = Texture(self.game.window, surf)

        self.add(Button(self, (400, 400), "Play", lambda: self.game.change_scene(levels[0](self.game))))

    def update(self, dt: float) -> None:
        self.sprite_manager.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        self.game.texture.blit(self.background, (0, 0))
        self.sprite_manager.draw(screen)
