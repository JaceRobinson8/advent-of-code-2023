from pathlib import Path
from dataclasses import dataclass
import logging
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class Card:
    id: int
    win_nums: list[int]
    other_nums: list[int]

    @classmethod
    def from_str(cls, card_line: str):
        id_str, nums_str = card_line.strip().split(": ")
        id = id_str.split(" ")[1]
        win_str, other_str = nums_str.split(" | ")
        win_nums = win_str.split(" ")
        win_nums = [
            int(num) for num in win_nums if num
        ]  # sometimes empty string, remove those with if
        other_nums = other_str.split(" ")
        other_nums = [
            int(num) for num in other_nums if num
        ]  # sometimes empty string, remove those with if
        return cls(id, win_nums, other_nums)

    def score(self) -> int:
        score = 0
        count = len(set(self.win_nums).intersection(set(self.other_nums)))
        if count > 0:
            score = 2 ** (count - 1)
        return score


def parse_input(file_path: Path = Path("./input/input.txt")) -> list[Card]:
    # First make grid
    with open(file_path, "r") as file:
        cards = [Card.from_str(line) for line in file.readlines()]
    return cards
