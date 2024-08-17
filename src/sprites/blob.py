from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import MainScene

from src.core.render_layer import Layer
from src.core.sprite import Sprite
from src.core.scene import Scene
from src.utils import Vec, Timer

from random import uniform
import pygame

class Blob(Sprite):
    def __init__(self, scene: Scene, pos: tuple[int, int], radius: int) -> None:
        super().__init__(scene, Layer.BLOB)
        self.scene: MainScene
        self.pos = Vec(pos)
        self.radius = radius

        self.scene.add_blob(self)

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        pass

    @property
    def data(self) -> tuple[int, int, int]:
        return self.pos.x, self.pos.y, self.radius

class ParticleBlob(Blob):
    def __init__(self, scene: Scene, pos: tuple[int, int], vel: tuple[float, float], radius: int) -> None:
        super().__init__(scene, pos, radius)
        self.scene: MainScene
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        self.max_radius = radius
        self.target_radius = radius
        self.radius = 0
        self.timer = Timer(lambda: uniform(1.2, 1.6))

        self.scene.add_blob(self)

    def update(self, dt: float) -> None:
        self.pos += self.vel * dt
        if self.radius < self.target_radius:
            self.radius += (self.target_radius - self.radius) * 0.03 * dt
        else:
            self.radius = self.target_radius
        self.target_radius = self.max_radius * (1 - self.timer.progress)

        if self.timer.ended():
            self.scene.remove_blob(self)

    def draw(self, screen: pygame.Surface) -> None:
        pass

    @property
    def data(self) -> tuple[int, int, int]:
        return self.pos.x, self.pos.y, self.radius
