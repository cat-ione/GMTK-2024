from src.core.glpg import Window, Texture, Shader
from src.scenes.main_menu import MainMenu
from src.scenes.level import levels
from src.core.scene import Scene

from pygame.locals import QUIT, SRCALPHA
import pygame

class AbortScene(Exception):
    def __str__(self):
        return "Scene aborted but not caught with a try/except block."

class AbortGame(Exception):
    def __str__(self):
        return "Game aborted but not caught with a try/except block."

class Game:
    def __init__(self) -> None:
        self.window = Window(800, 800)
        self.screen = pygame.Surface((800, 800), SRCALPHA)
        self.shader = Shader(self.window, "assets/shaders/post.frag")
        self.texture = Texture(self.window, self.screen, self.shader)
        self.clock = pygame.time.Clock()

        self.dt = self.clock.tick(60) * 0.05
        self.scene = MainMenu(self)

    def run(self) -> None:
        while True:
            try:
                self.update()
                self.scene.update(self.dt)
            except AbortScene:
                continue
            except AbortGame:
                break

            self.scene.draw(self.screen)
            self.window.blit(self.texture, (0, 0))
            pygame.display.flip()

            pygame.display.set_caption(f"Umbral | FPS: {self.clock.get_fps():.0f}")

            self.dt = self.clock.tick(0) * 0.05

        pygame.quit()

    def update(self) -> None:
        self.events = {event.type: event for event in pygame.event.get()}

        if QUIT in self.events:
            raise AbortGame

    def change_scene(self, scene: Scene | str) -> None:
        if isinstance(scene, str):
            self.scene = eval(scene)(self)
            return
        self.scene = scene
