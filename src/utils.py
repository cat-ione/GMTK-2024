from multimethod import multimeta
from pygame.math import Vector2
from typing import Self
from math import floor

def read_file(path: str) -> str:
    """Opens a file, read the contents of the file, then closes it.

    Args:
        path: The path of the file to read from.

    Returns:
        The full contents of the file.
    """
    with open(path, "r") as file:
        return file.read()

def inttup(tup: tuple[float, float]) -> tuple:
    """Convert a tuple of 2 floats to a tuple of 2 ints.

    Args:
        tup: The tuple to convert.

    Returns:
        The integer tuple.
    """
    return (floor(tup[0]), floor(tup[1]))

class Vec(Vector2, metaclass=multimeta):
    def normalize(self) -> Self:
        try:
            return super().normalize()
        except ValueError:
            return Vec(0, 0)

    def normalize_ip(self) -> None:
        try:
            return super().normalize_ip()
        except ValueError:
            pass

    def clamp_magnitude(self, max_length: float) -> Self:
        try:
            return super().clamp_magnitude(max_length)
        except ValueError:
            return Vec(0, 0)

    def clamp_magnitude(self, min_length: float, max_length: float) -> Self:
        try:
            return super().clamp_magnitude(min_length, max_length)
        except ValueError:
            return Vec(0, 0)

    def clamp_magnitude_ip(self, max_length: float) -> None:
        try:
            return super().clamp_magnitude_ip(max_length)
        except ValueError:
            pass

    def clamp_magnitude_ip(self, min_length: float, max_length: float) -> None:
        try:
            return super().clamp_magnitude_ip(min_length, max_length)
        except ValueError:
            pass

    def __hash__(self) -> int:
        return tuple(self).__hash__()
