from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game

from src.sprites.blob import Blob, ParticleBlob
from src.core.glpg import Texture, Shader
from src.core.scene import Scene
import src.assets as assets

from random import randint, uniform
from math import pi, cos, sin
import pygame

class MainScene(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__(game)
        self.blob_shader = Shader(game.window, "assets/shaders/metaball.frag")
        surf = pygame.Surface(game.window.size, pygame.SRCALPHA)
        self.blob_texture = Texture(game.window, surf, self.blob_shader)

        self.blobs = []
        self.blob_count = 0
        Blob(self, (400, 400), 200)

    def update(self, dt: float) -> None:
        if randint(0, 100) < 5:
            angle = uniform(0, 2 * pi)
            x, y = 400 + 100 * cos(angle), 400 + 100 * sin(angle)
            ParticleBlob(self, (x, y), (cos(angle + randint(-10, 10)), sin(angle + randint(-10, 10))), randint(2, 12))

        self.blob_shader.send("u_metaballCount", self.blob_count)
        self.blob_shader.send("u_metaballs", [self.blobs[i].data if i < len(self.blobs) else (0, 0, 0) for i in range(500)])

        self.sprite_manager.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        self.game.window.blit(self.blob_texture, (0, 0))
        self.sprite_manager.draw(screen)

    def add_blob(self, blob: Blob) -> None:
        self.blobs.append(blob)
        self.add(blob)
        self.blob_count += 1

    def remove_blob(self, blob: Blob) -> None:
        self.blobs.remove(blob)
        self.remove(blob)
        self.blob_count -= 1
