from pathlib import Path
from dataclasses import dataclass, field
import logging
from collections import Counter

logger = logging.getLogger(__name__)


class Round:
    hand: str  # e.g. length 5 string AAAK2
    bid: int  # e.g. 324

    def __init__(self, hand: str, bid: str):
        self.hand = hand
        self.bid = int(bid)

    @property
    def strength(self):
        pass

    def __str__(self):
        return self.hand

    def __repr__(self):
        return self.hand


@dataclass
class Game:
    rounds: list[Round]

    def __str__(self):
        return self.rounds

    def __repr__(self):
        return self.rounds


def key(round: Round) -> str:
    # To sort, lets create a string as the key
    # separate by underscore to make easier to debug
    # Left most digit is most significant digit 1-7 for high card to five of a kind.
    # right digits are 0-12 for 2 to Ace for each position ()
    return _left_sig(handle_jokers(round.hand)) + "_" + _right_sig(round.hand)


def handle_jokers(hand: str) -> str:
    # Joker always converts to most common hand
    most_common_list = Counter(hand).most_common(2)
    top_letter, top_count = most_common_list[0]
    if (
        top_letter == "J" and top_count < 5
    ):  # special case if joker most common letter and not 5 jokers
        top_letter = most_common_list[1][0]  # use second most common letter instead

    return hand.replace("J", top_letter)


def _left_sig(hand: str) -> str:
    # ranking of hands
    most_common_list = Counter(hand).most_common(2)
    top_count = most_common_list[0][1]
    if len(most_common_list) > 1:
        second_count = most_common_list[1][1]
    else:
        second_count = 0

    if top_count == 5:  # five of kind
        left_sig = "7"
    elif top_count == 4:  # four of kind
        left_sig = "6"
    elif top_count == 3 and second_count == 2:  # full house
        left_sig = "5"
    elif top_count == 3:  # three of a kind
        left_sig = "4"
    elif top_count == 2 and second_count == 2:  # two pair
        left_sig = "3"
    elif top_count == 2:  # 1 pair
        left_sig = "2"
    else:  # high card
        left_sig = "1"
    return left_sig


def _right_sig(hand: str) -> str:
    # tie breaking for hands of same type
    # use the index to determine the key, with 2 (index 0) and A (index 12)
    values = "J23456789TQKA"
    return "_".join([str(values.find(c)).zfill(2) for c in hand])  # use index to rank


def parse_input(file_path: Path = Path("./input/input.txt")) -> Game:
    with open(file_path, "r") as file:
        return Game([Round(*line.strip().split(" ")) for line in file.readlines()])
