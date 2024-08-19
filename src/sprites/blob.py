from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Level

from src.core.render_layer import Layer
from src.core.sprite import Sprite
from src.core.scene import Scene
from src.utils import Vec, Timer

from random import uniform, randint
from math import exp2
import pygame

class Blob(Sprite):
    def __init__(self, scene: Scene, pos: tuple[int, int], radius: int, antiball: bool = False) -> None:
        super().__init__(scene, Layer.BLOB)
        self.scene: Level
        self.pos = Vec(pos)
        self.radius = radius
        self.antiball = antiball

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
        self.scene: Level
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        self.max_radius = radius
        self.target_radius = radius
        self.radius = 0
        self.timer = Timer(lambda: uniform(1.2, 1.6))
        self.timer.start()

        self.scene.add_blob(self)

    def update(self, dt: float) -> None:
        self.pos += self.vel * dt
        if self.radius < self.target_radius:
            self.radius += (self.target_radius - self.radius) * 0.03 * dt
        else:
            self.radius = self.target_radius
        self.target_radius = self.max_radius * (1 - self.timer.progress)

        if not (-self.radius < self.pos.x < self.scene.game.window.size[0] + self.radius \
                and -self.radius < self.pos.y < self.scene.game.window.size[1] + self.radius):
            self.scene.remove_blob(self)
            return

        if self.timer.ended():
            self.scene.remove_blob(self)

class DragInducedBlob(Blob):
    def __init__(self, scene: Scene, pos: tuple[int, int], radius: int) -> None:
        super().__init__(scene, pos, radius)
        self.dragging = True

    def update(self, dt: float) -> None:
        if self.dragging: return
        self.radius -= 2.0 * dt
        if self.radius <= 0:
            self.scene.remove_blob(self)

class DragInducedAntiBlob(Blob):
    def __init__(self, scene: Scene, pos: tuple[int, int], radius: int) -> None:
        super().__init__(scene, pos, radius, antiball=True)
        self.dragging = True

    def update(self, dt: float) -> None:
        if self.dragging: return
        self.radius -= 0.04 * dt
        self.scene.expand_speed += 0.0000025 * dt
        if self.radius <= 0:
            self.scene.remove_blob(self)

class BulletBlob(Blob):
    def __init__(self, scene: Scene, pos: tuple[int, int]) -> None:
        super().__init__(scene, pos, randint(15, 25))
        self.scene: Level
        self.orig_offset = Vec(pos) - Vec(400, 400)
        self.direction = (Vec(400, 400) - Vec(pos)).normalize()
        self.linear_scale = 0
        self.scale = exp2(self.linear_scale)
        self.has_captured = False
        self.capture_timer = Timer(lambda: 5.0)

    def update(self, dt: float) -> None:
        self.linear_scale -= self.scene.zoom_speed * dt
        self.scale = exp2(self.linear_scale)
        self.pos = Vec(400, 400) + self.orig_offset * self.scale

        if self.has_captured:
            mpos = Vec(pygame.mouse.get_pos())
            pygame.mouse.set_pos(mpos + (self.pos - mpos) * 0.1)
            self.linear_scale -= 0.08 * dt
            if self.capture_timer.ended():
                self.scene.remove_blob(self)
                self.scene.captured = False
                self.scene.invulnerable_timer.reset()
                return

        if self.pos.distance_to(pygame.mouse.get_pos()) < self.radius and not self.has_captured \
            and self.pos.distance_to(Vec(400, 400)) > self.scene.main_blob.radius / 2 \
                and self.scene.invulnerable_timer.ended():
            self.has_captured = True
            self.scene.captured = True
            self.capture_timer.start()

        if self.pos.distance_to((400, 400)) < self.scene.main_blob.radius / 2 and not self.has_captured:
            self.scene.remove_blob(self)
