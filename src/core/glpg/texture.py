from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .window import Window

from src.core._types import ColorType, RectType
from src.core.glpg.shader import Shader
from src.utils import inttup

from typing import Optional
from src.utils import Vec
import moderngl
import struct
import pygame

class Texture:
    """Wrapper for a ModernGL Texture, FBO, and VAO. This class allows
    other textures to be rendered onto it, and can be rendered onto the
    parent window.

    Args:
        window: The parent window object.
        src: The source of the texture, either a file path or a pygame
            Surface object.
        shader: The shader object to render the texture with. Defaults
            to a new shader object.
    """

    def __init__(self, window: Window, src: pygame.Surface | str,
                 shader: Optional[Shader] = None) -> None:
        self.window = window
        self.shader = shader if shader is not None else Shader(window)
        self.ctx = window.ctx
        if isinstance(src, str):
            src = pygame.image.load(src).convert_alpha()
        self.surf = pygame.transform.flip(src, False, True)
        self.size = Vec(self.surf.get_size())

        texture = self.ctx.texture(inttup(self.size), 4,
                                   self.surf.get_view())
        texture.repeat_x = texture.repeat_y = False
        texture.swizzle = "BGRA"
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.fbo = self.ctx.framebuffer([texture])

        vbo = self.ctx.buffer(struct.pack("8f",
                                          0,           0,
                                          self.size.x, 0,
                                          0,           self.size.y,
                                          self.size.x, self.size.y))
        vao_content = [(vbo, "2f", "vertexPos"),
                       (self.window.uvmap, "2f", "vertexTexCoord")]
        self.vao = self.ctx.vertex_array(self.shader.program,
                                         vao_content,
                                         self.window.ibo)

    def move(self, pos: tuple[int, int]) -> None:
        """Set the position where the Texture will be rendered. This is
        where the topleft corner of the Texture will be.

        Args:
            pos: The coordinates of the topleft corner.
        """
        self.shader.move(pos)

    @property
    def texture(self) -> moderngl.Texture:
        """Retrieve the Texture object (the color attachment) of the
        framebuffer.

        Returns:
            The Texture object.
        """
        return self.fbo.color_attachments[0]

    def blit(self, texture: Texture, pos: tuple[int, int]) -> None:
        """Render another Texture onto this Texture.

        Args:
            texture: The Texture to render.
            pos: Position of the topleft vertex of the Texture.
        """
        self.fbo.use()
        texture.texture.use()
        texture.texture.swizzle = "RGBA"
        texture.shader.send("u_targetSize", self.size)
        texture.shader.send("u_texSize", texture.size)
        texture.move(pos)
        texture.vao.render()

    def fill(self, color: ColorType, rect: Optional[RectType] = None) -> None:
        """Fill the entire Texture or parts of the Texture with a given
        color.

        Args:
            color: The color value to fill the Texture with.
            rect: The area of the texture to fill. Defaults to the whole
                Texture.
        """
        color = color[::-1] + (255,) if len(color) == 3 else color[2::-1] + (color[-1],)
        if rect:
            rect = list(inttup(rect))
            rect[1] = int(self.size.y - rect[1] - rect[3])
        else:
            rect = [0, 0, *inttup(self.size)]
        data = bytes(color * rect[2] * rect[3])
        self.texture.write(data, tuple(rect))

    def update(self, src: pygame.Surface) -> None:
        """Update the Texture with a new source.

        Args:
            src: The new source of the Texture.
        """
        self.surf = src
        self.size = Vec(self.surf.get_size())
        self.texture.write(pygame.image.tostring(self.surf, "BGRA", True))
