from pathlib import Path
from dataclasses import dataclass
import logging
from math import sqrt, floor, ceil
import re

logger = logging.getLogger(__name__)


@dataclass
class Race:
    time: int
    record_distance: int

    @property
    def beat_record_count(self) -> int:
        # the boat problem forms a quadratic equation
        # The "winning" solutions are the count of integer x values between zeros of the quadratic.
        x = quadratic_solver(1.0, -1.0 * self.time, float(self.record_distance))
        # want to be NOT inclusive on the ends, if I didn't need to round, reduce by 1
        if floor(x[1]) < x[1]:
            x1 = floor(x[1])
        else:
            x1 = floor(x[1]) - 1

        if ceil(x[0]) > x[0]:
            x0 = ceil(x[0])
        else:
            x0 = ceil(x[0]) + 1
        return x1 - x0 + 1


def quadratic_solver(a: float, b: float, c: float) -> list:
    x1 = (-1 * b + sqrt(b**2 - 4 * a * c)) / (2 * a)
    x2 = (-1 * b - sqrt(b**2 - 4 * a * c)) / (2 * a)
    res = [x1, x2]
    res.sort()
    return res


def parse_input(file_path: Path = Path("./input/input.txt")) -> list[Race]:
    # regex to find all digits in a line
    pattern = re.compile("\d+")
    # First make grid
    with open(file_path, "r") as file:
        # get times
        times = pattern.findall(file.readline())
        # get distances
        distances = pattern.findall(file.readline())
        # organize into races
        races = [
            Race(time=int(t), record_distance=int(d)) for t, d in zip(times, distances)
        ]
    return races
