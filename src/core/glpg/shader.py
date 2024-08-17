from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .window import Window

from src.utils import read_file

from typing import Optional

DEFAULT_FRAG = "assets/shaders/default.frag"
DEFAULT_VERT = "assets/shaders/default.vert"

class Shader:
    def __init__(self, window: Window, frag: Optional[str] = DEFAULT_FRAG,
                 vert: Optional[str] = DEFAULT_VERT) -> None:
        """Wrapper for a ModernGL shader program.

        Args:
            window (Window): The main window object
            frag (str, optional): Path of the fragment shader source. Defaults to DEFAULT_FRAG
            vert (str, optional): Path of the vertex shader source. Defaults to DEFAULT_VERT
        """
        self.window = window
        self.vert = read_file(vert)
        self.frag = read_file(frag)
        self.program = window.ctx.program(vertex_shader=self.vert, fragment_shader=self.frag)

    def send(self, name: str, value: float | tuple[float, float]) -> None:
        """Send a uniform variable to the shader.

        Args:
            name (str): The name of the uniform variable
            value (float | tuple[float, float]): The value of the variable
        """
        try:
            self.program[name].value = value if isinstance(value, (float, int)) else tuple(value)
        except KeyError:
            pass

    def get(self, name: str) -> float | tuple[float, float]:
        """Get the value of a uniform variable previously sent to the shader.

        Args:
            name (str): The name of the uniform variable

        Returns:
            float | tuple[float, float]: The value of the uniform variable
        """
        return self.program[name].value

    def move(self, pos: tuple[int, int]) -> None:
        """Prepare the shader to render with an offset next time.

        Args:
            pos (tuple[int, int]): The offset of the topleft vertex
        """
        self.send("u_vertexOffset", pos)
