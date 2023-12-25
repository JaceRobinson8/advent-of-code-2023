from pathlib import Path
from dataclasses import dataclass
import logging
from enum import StrEnum, auto

logger = logging.getLogger(__name__)


class Colors(StrEnum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()


@dataclass
class Round:
    red: int = 0
    blue: int = 0
    green: int = 0

    @classmethod
    def from_str(cls, round_str: str):
        round = cls()
        [
            round.set_count_from_str(*count_str.split(" "))
            for count_str in round_str.split(", ")
        ]
        return round

    def set_count_from_str(self, count: str, color: str) -> None:
        vars(self)[color] = int(count)

    def check_possible(self, n_red_max: int, n_green_max: int, n_blue_max: int) -> bool:
        # Game possible if real values less than equal to ALL provided values
        logger.debug(f"r: {self.red}, g: {self.green}, b: {self.blue}")
        return (
            self.red <= n_red_max
            and self.green <= n_green_max
            and self.blue <= n_blue_max
        )


@dataclass
class Game:
    id: int
    rounds: list[Round]

    @classmethod
    def from_str(cls, game_str: str):
        g_id_str, rounds_str = game_str.strip().split(": ")
        return cls(
            id=int(g_id_str.split(" ")[1]),
            rounds=[Round.from_str(round_str) for round_str in rounds_str.split("; ")],
        )

    def check_possible(self, n_red_max: int, n_green_max: int, n_blue_max: int) -> bool:
        return all(
            [r.check_possible(n_red_max, n_green_max, n_blue_max) for r in self.rounds]
        )


def parse_input(file_path: Path = Path("./input/input.txt")) -> list[Game]:
    with open(file_path, "r") as file:
        lines = file.readlines()
        games = [Game.from_str(line) for line in lines]
    return games
