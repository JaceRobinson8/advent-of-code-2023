from pathlib import Path
from dataclasses import dataclass
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class Colors(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class Round:
    n_red: int = 0
    n_blue: int = 0
    n_green: int = 0

    def __init__(self, r: str):
        colors = [x.split(" ") for x in r.split(", ")]
        for color in colors:
            if color[1] == Colors.RED:
                self.n_red = int(color[0])
            elif color[1] == Colors.GREEN:
                self.n_green = int(color[0])
            elif color[1] == Colors.BLUE:
                self.n_blue = int(color[0])


@dataclass
class Game:
    id: int
    rounds: list[Round]

    # @property
    # def cal_val(self) -> int:
    #     digits = [char for char in self.raw if char.isdigit()]
    #     return int(digits[0] + digits[-1])


def parse_input(file_path: Path = Path("./input/input.txt")) -> list[Game]:
    with open(file_path, "r") as file:
        lines = file.readlines()
        games = []
        for line in lines:
            line = line.strip()  # remove new line
            game, r_str = line.split(": ")  # separate game from rounds
            games.append(
                Game(
                    id=game.split(" ")[-1], rounds=[Round(r) for r in r_str.split("; ")]
                )
            )
            logger.info("Game:")
            logger.info(Game)
        # data = [Game(row[0]) for row in reader]
    return games
