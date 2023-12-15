from pathlib import Path
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class Card:
    id: int
    win_nums: list[int]
    other_nums: list[int]

    @classmethod
    def from_str(cls, card_line: str):
        id_str, nums_str = card_line.strip().split(": ")
        id = int(id_str.split(" ")[-1])
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

    @property
    def win_card_idx(self) -> list[int]:
        win_size = len(set(self.win_nums).intersection(set(self.other_nums)))
        return list(range(1, win_size + 1))

    def play(self) -> list[int]:
        # recursive function
        # logger.debug(f"id: {self.id}")
        winners = self.win_card_idx
        # logger.debug(f"win_card_idx: {winners}")
        return winners


@dataclass
class CardStack:
    cards: list[Card]

    def start(self) -> int:
        return sum([self.recurse(idx) for idx, c in enumerate(self.cards)])

    def recurse(self, c_id: int) -> int:
        # base case 1: card past end of table
        if c_id >= len(self.cards):
            return 0

        winners = self.cards[c_id].play()
        # logger.debug(f"id: {c_id}")
        # logger.debug(f"len(winners): {len(winners)}")
        # base case 2: card is not a winner
        if not winners:
            return 1

        # recurse: card is a winner
        return sum([self.recurse(c_id + winner) for winner in winners]) + 1


def parse_input(file_path: Path = Path("./input/input.txt")) -> CardStack:
    # First make grid
    with open(file_path, "r") as file:
        return CardStack([Card.from_str(line) for line in file.readlines()])
