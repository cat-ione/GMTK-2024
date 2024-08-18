from src.exe import pathof

from multimethod import multimeta
from pygame.math import Vector2
from typing import Callable
from typing import Self
from math import floor
import time

def read_file(path: str) -> str:
    """Opens a file, read the contents of the file, then closes it.

    Args:
        path: The path of the file to read from.

    Returns:
        The full contents of the file.
    """
    with open(pathof(path), "r") as file:
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

class Timer:
    def __init__(self, time_func: Callable[[], float]) -> None:
        self.time_func = time_func
        self.total_time = time_func()
        self.start_time = time.time()

    def ended(self) -> bool:
        return time.time() - self.start_time >= self.total_time

    def ended_and_reset(self) -> int:
        # If the timer has ended, return how many times it has ended since the last call, and reset the timer.
        if self.ended():
            ended = floor((time.time() - self.start_time) / self.total_time)
            self.start_time += ended * self.total_time
            return ended
        return 0

    def reset(self) -> None:
        self.start_time = time.time()
        self.total_time = self.time_func()

    @property
    def progress(self) -> float:
        return (time.time() - self.start_time) / self.total_time
