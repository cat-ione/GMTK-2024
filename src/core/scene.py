from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game import Game

from src.core.sprite_manager import SpriteManager
from src.core.sprite import Sprite

from abc import ABC as AbstractClass, abstractmethod
import pygame

class Scene(AbstractClass):
    def __init__(self, game: Game) -> None:
        self.game = game
        self.sprite_manager = SpriteManager()

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        pass

    def add(self, sprite: Sprite) -> None:
        self.sprite_manager.add(sprite)

    def remove(self, sprite: Sprite) -> None:
        self.sprite_manager.remove(sprite)
