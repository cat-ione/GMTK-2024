from src.core.render_layer import RenderLayer, Layer
from src.core.sprite import Sprite

import pygame

class SpriteManager:
    def __init__(self) -> None:
        self.layers = {layer: RenderLayer() for layer in Layer}

    def update(self, dt: float) -> None:
        for layer in self.layers.values():
            layer.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        for layer in self.layers.values():
            layer.draw(screen)

    def add(self, sprite: Sprite) -> None:
        self.layers[sprite.layer].add(sprite)

    def remove(self, sprite: Sprite) -> None:
        self.layers[sprite.layer].remove(sprite)
