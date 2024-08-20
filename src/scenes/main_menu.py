from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game

from src.scenes.level_selection import LevelSelection
from src.sprites.button import Button
from src.core.glpg import Texture
from src.core.scene import Scene
import src.assets as assets
from src.exe import pathof

from pygame.locals import SRCALPHA
import pygame

class MainMenu(Scene):
    def __init__(self, game: Game) -> None:
        super().__init__(game)

        surf = pygame.Surface(self.game.window.size, SRCALPHA)
        surf.fill((0, 0, 0, 255))
        self.background = Texture(self.game.window, surf)

        self.gamma_index = 1
        self.gamma_levels = [0.75, 1.0, 1.6, 2.2, 2.8]
        self.gamma_hints = ["Spookily Dark", "Dark: Best for OLEDs", "Bright", "Very Bright: Good for most other monitors", "Blindingly Bright: Why?"]
        self.add(Button(self, (400, 400), "Play", 50, lambda: self.game.change_scene(LevelSelection(self.game))))
        self.add(Button(self, (280, 650), "–", 80, self.decrease_gamma, scale=0.5))
        self.add(Button(self, (520, 650), "+", 80, self.increase_gamma, scale=0.5))
        self.gamma_texture = Texture(self.game.window, assets.fonts[34].render(str(self.gamma_levels[self.gamma_index]), True, (222, 222, 222)))
        self.gamma_hint_texture = Texture(self.game.window, assets.fonts[18].render(self.gamma_hints[self.gamma_index], True, (222, 222, 222)))

    def update(self, dt: float) -> None:
        self.sprite_manager.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        self.game.texture.blit(self.background, (0, 0))
        self.sprite_manager.draw(screen)
        self.game.texture.blit(self.gamma_texture, ((self.game.window.size[0] - self.gamma_texture.size[0]) // 2, 633))
        self.game.texture.blit(self.gamma_hint_texture, ((self.game.window.size[0] - self.gamma_hint_texture.size[0]) // 2, 720))

    def increase_gamma(self) -> None:
        if self.gamma_index < len(self.gamma_levels) - 1:
            self.gamma_index += 1
            self.gamma_texture = Texture(self.game.window, assets.fonts[34].render(str(self.gamma_levels[self.gamma_index]), True, (222, 222, 222)))
            self.gamma_hint_texture = Texture(self.game.window, assets.fonts[18].render(self.gamma_hints[self.gamma_index], True, (222, 222, 222)))
            self.game.shader.send("u_gamma", self.gamma_levels[self.gamma_index])

    def decrease_gamma(self) -> None:
        if self.gamma_index > 0:
            self.gamma_index -= 1
            self.gamma_texture = Texture(self.game.window, assets.fonts[34].render(str(self.gamma_levels[self.gamma_index]), True, (222, 222, 222)))
            self.gamma_hint_texture = Texture(self.game.window, assets.fonts[18].render(self.gamma_hints[self.gamma_index], True, (222, 222, 222)))
            self.game.shader.send("u_gamma", self.gamma_levels[self.gamma_index])
