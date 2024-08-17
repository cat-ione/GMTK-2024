from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .texture import Texture

from src.core._types import ColorType

from pygame.locals import *
import moderngl
import struct
import pygame
import os

class Window:
    def __init__(self, width: int, height: int) -> None:
        """Wrapper for Pygame window and ModernGL context.

        Args:
            width (int): Width of the window
            height (int): Height of the window
        """
        os.environ["SDL_VIDEO_WINDOW_POS"] = "200,200"
        self.width, self.height = self.size = width, height
        pygame.init()
        self.display = pygame.display.set_mode((width, height), HWSURFACE | DOUBLEBUF | OPENGL)
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.BLEND)

        self.uvmap = self.ctx.buffer(struct.pack("8f", *[0, 1, 1, 1, 0, 0, 1, 0]))
        self.ibo = self.ctx.buffer(struct.pack("6I", *[0, 1, 2, 1, 2, 3]))

    def blit(self, texture: Texture, pos: tuple[int, int]) -> None:
        """Render a texture onto the window default framebuffer.

        Args:
            texture (Texture): The texture to render onto the default framebuffer (window)
            pos (tuple[int, int]): The topleft position to render the texture
        """
        self.ctx.screen.use()
        texture.texture.use()
        texture.shader.send("u_targetSize", self.size)
        texture.shader.send("u_texSize", texture.size)
        texture.move(pos)
        texture.vao.render()

    def fill(self, color: ColorType) -> None:
        """Fill the default framebuffer with the specified color.

        Args:
            color (_Color): The color to fill the framebuffer with (window)
        """
        self.ctx.screen.use()
        self.ctx.clear(*map(lambda x: x / 255, color))
