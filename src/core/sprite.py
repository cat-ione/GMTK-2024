from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.render_layer import Layer
    from src.core.scene import Scene

from abc import ABC as AbstractClass, abstractmethod
from typing import Self
from uuid import uuid4
import pygame

class Sprite(AbstractClass):
    def __init__(self, scene: Scene, layer: Layer) -> None:
        self.uuid = uuid4()
        self.scene = scene
        self.layer = layer

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        pass

    def bind(self, sprite: Self) -> None:
        self.scene.sprite_manager.layers[self.layer].bind(sprite, self)

    def __hash__(self) -> int:
        return hash(self.uuid)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}{{{self.uuid}}}"
