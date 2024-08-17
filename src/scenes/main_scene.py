from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game

from src.core.scene import Scene
import src.assets as assets

import pygame

class MainScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__(game)

    def update(self, dt: float) -> None:
        self.sprite_manager.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill((50, 50, 50))
        self.sprite_manager.draw(screen)
