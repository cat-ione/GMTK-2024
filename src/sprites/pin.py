from src.core.render_layer import Layer
from src.core.sprite import Sprite
from src.core.scene import Scene
from src.utils import Vec, Timer

from random import uniform, randint
import pygame

class Pin(Sprite):
    def __init__(self, scene: Scene, pos: tuple[int, int]) -> None:
        super().__init__(scene, Layer.PIN)
        self.pos = Vec(pos)
        self.pos2 = Vec(pos)
        self.held = True
        self.settled = False

    def update(self, dt: float) -> None:
        if not pygame.mouse.get_pressed()[0]:
            self.held = False

        if self.held:
            self.pos = Vec(pygame.mouse.get_pos())
        else:
            self.pos += (Vec(400, 400) - self.pos).normalize() * 40 * dt

        if self.pos.distance_to(Vec(400, 400)) < self.scene.main_blob.radius:
            self.pos = Vec(400, 400) + (self.pos - Vec(400, 400)).normalize() * self.scene.main_blob.radius
            self.held = False
            self.settled = True

        self.pos2 = self.pos - (Vec(400, 400) - self.pos).normalize() * 80

        for pin in self.scene.pins:
            if pin == self: continue
            if self.pos.distance_to(pin.pos2) < 8 or self.pos2.distance_to(pin.pos2) < 12:
                self.scene.remove_pin(self)
                self.scene.remove_pin(pin)
        if self.pos2.distance_to(pygame.mouse.get_pos()) < 8 and self.settled:
            self.scene.remove_pin(self)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.line(screen, (222, 222, 222), self.pos, self.pos2, 5)
        pygame.draw.circle(screen, (222, 222, 222), self.pos2, 8)

class PinParticle(Sprite):
    def __init__(self, scene: Scene, pos: tuple[int, int]) -> None:
        super().__init__(scene, Layer.PIN)
        self.pos = Vec(pos)
        self.vel = (Vec(400, 400) - self.pos).normalize().rotate(randint(-20, 20)) * uniform(3, 8)
        self.pos2 = Vec(pos)
        self.timer = Timer(lambda: uniform(0.3, 0.6))
        self.timer.start()

    def update(self, dt: float) -> None:
        if self.timer.ended_and_reset():
            self.scene.remove(self)

        self.pos -= self.vel * dt
        self.pos2 = self.pos - (Vec(400, 400) - self.pos).normalize() * 10

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.line(screen, (222, 222, 222, min(255, max(0, (1 - self.timer.progress) * 255))), self.pos, self.pos2, 3)
