from pathlib import Path
from dataclasses import dataclass
import logging
from itertools import pairwise

logger = logging.getLogger(__name__)


def check_all_zero(seq: list[int]) -> bool:
    return all([x == 0 for x in seq])


@dataclass
class SequenceStack:  # a single input line
    seqs: list[list[int]]

    @classmethod
    def from_str(cls, text_line: str):
        """Initialize original sequence as list of list of int"""
        return cls(seqs=[[int(x) for x in text_line.strip().split(" ")]])

    def build_diff_seqs(self) -> None:
        """Given initial sequence, build difference sequences."""
        assert len(self.seqs) >= 1  # check seqs has been initialized
        while not check_all_zero(self.seqs[-1]):  # continue until last seq all zero
            self.seqs.append(
                [second - first for first, second in pairwise(self.seqs[-1])]
            )  # build new seq of differences

    def append_stack(self) -> None:
        """Starting at bottom of stack, append one new value on each sequence"""
        assert len(self.seqs) >= 2  # must be at least 2 sequences from build_stack()
        new_val = 0  # initial seq appends 0
        # reverse to go bottom up
        for bot_seq, top_seq in pairwise(reversed(self.seqs)):
            bot_seq.append(new_val)
            # last number of current sequence + last number in previous seq
            new_val = top_seq[-1] + bot_seq[-1]
        top_seq.append(new_val)

    @property
    def top_extrap_val(self) -> int:
        """Return last value of first sequence"""
        return self.seqs[0][-1]


def parse_input(file_path: Path = Path("./input/input.txt")) -> list[SequenceStack]:
    # First make grid
    with open(file_path, "r") as file:
        stacks = [SequenceStack.from_str(line) for line in file.readlines()]
        for stack in stacks:
            stack.build_diff_seqs()
            stack.append_stack()
        logger.debug(stacks)

    return stacks
