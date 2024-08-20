from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.scenes.level import Level1

from src.core.render_layer import Layer
from src.core.sprite import Sprite
from src.core.scene import Scene
from src.utils import Timer
import src.assets as assets
from src.utils import Vec

from math import exp2, atan2, degrees, floor
from random import uniform
import pygame

class Ink(Sprite):
    def __init__(self, scene: Scene) -> None:
        super().__init__(scene, Layer.INK)
        self.scene: Level1

        self.drawing = True
        self.draw_timer = Timer(lambda: 0.01)
        self.draw_timer.start()
        self.linear_scale = 0
        self.scale = exp2(self.linear_scale)
        self.points: list[Vec] = []
        self.settled = False
        self.prev_settled = False
        self.closed = False
        self.present_coverage = 0
        self.has_landed = False
        self.sizzle_timer = Timer(lambda: uniform(1.5, 2.2))
        self.sizzle_timer.start()
        assets.ink.set_volume(0)
        assets.ink.play()

    def update(self, dt: float) -> None:
        if not pygame.mouse.get_pressed()[0]:
            self.drawing = False
            assets.ink.fadeout(400)

        if self.drawing:
            if assets.ink.get_volume() < 0.3:
                assets.ink.set_volume(assets.ink.get_volume() + 0.05 * dt)
            if self.sizzle_timer.ended_and_reset():
                assets.ink.play()
            if self.draw_timer.ended_and_reset():
                mpos = Vec(pygame.mouse.get_pos())
                point = mpos - Vec(400, 400)
                if self.points:
                    diff = point - self.points[-1]
                    for i in range(int(diff.length()), 0, -10):
                        self.points.append(point - diff.normalize() * i)
                self.points.append(point)
            return

        self.linear_scale -= self.scene.zoom_speed * dt
        self.scale = exp2(self.linear_scale)

        if not self.prev_settled and self.settled:
            for point in self.points:
                angle = floor(degrees(atan2(point.y, point.x)) / 15) * 15
                if angle == 180: angle = -180
                if self.scene.covered_angles[angle] <= self.scene.angle_coverage // 24:
                    self.scene.covered_angles[angle] += 1

    def draw(self, screen: pygame.Surface) -> None:
        if len(self.points) < 2: return
        new_points = []
        self.prev_settled = self.settled
        self.settled = True
        for point in self.points:
            offset = point * self.scale
            min_offset = self.scene.main_blob.radius * 1.25 + self.present_coverage // 24 * 8
            if offset.length() > min_offset:
                self.settled = False
            else:
                offset.clamp_magnitude_ip(min_offset, 9999999.)
                if not self.has_landed:
                    self.present_coverage = self.scene.angle_coverage
                    self.has_landed = True
            new_points.append(Vec(400, 400) + offset)
        pygame.draw.lines(screen, (222, 222, 222), self.closed, new_points, 10)
