from pathlib import Path
from dataclasses import dataclass
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class Colors(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


@dataclass
class Round:
    n_red: int = 0
    n_blue: int = 0
    n_green: int = 0

    @classmethod
    def from_str(cls, round_str: str):
        round = cls()
        [round.set_count_from_str(count_str) for count_str in round_str.split(", ")]
        return round

    def set_count_from_str(self, count_str: str) -> None:
        count, color = count_str.split(" ")
        match color:
            case Colors.RED.value:
                self.n_red = int(count)
            case Colors.GREEN.value:
                self.n_green = int(count)
            case Colors.BLUE.value:
                self.n_blue = int(count)
            case _:
                raise ValueError("Invalid color str")

    def check_possible(self, n_red_max: int, n_green_max: int, n_blue_max: int) -> bool:
        # Game possible if real values less than equal to ALL provided values
        logger.debug(f"r: {self.n_red}, g: {self.n_green}, b: {self.n_blue}")
        return (
            self.n_red <= n_red_max
            and self.n_green <= n_green_max
            and self.n_blue <= n_blue_max
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

    def get_power(self) -> int:
        return self.get_max_red() * self.get_max_green() * self.get_max_blue()

    def get_max_red(self) -> int:
        return max([r.n_red for r in self.rounds])

    def get_max_green(self) -> int:
        return max([r.n_green for r in self.rounds])

    def get_max_blue(self) -> int:
        return max([r.n_blue for r in self.rounds])


def parse_input(file_path: Path = Path("./input/input.txt")) -> list[Game]:
    with open(file_path, "r") as file:
        lines = file.readlines()
        games = [Game.from_str(line) for line in lines]
    return games
