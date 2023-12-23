from pathlib import Path
from dataclasses import dataclass, field
import logging
import re
from enum import Enum, auto

logger = logging.getLogger(__name__)


class Instruction(Enum):
    LEFT = auto()
    RIGHT = auto()


@dataclass
class Node:
    key: str

    def __hash__(self):
        return hash(self.key)

    def __str__(self):
        return self.key

    def __repr__(self):
        return self.key


@dataclass
class Direction:
    left: Node
    right: Node

    def __str__(self):
        return f"({self.left}, {self.right})"

    def __repr__(self):
        return f"({self.left}, {self.right})"

    def get_next_loc(self, dir: str) -> Node:
        return self.left if dir == Instruction.LEFT else self.right


@dataclass
class Map:
    current_loc: Node
    dirs: dict[Node, Direction]  # each location

    @classmethod
    def from_str(cls, my_str: str):
        return cls(
            Node("AAA"),
            {Node(line[0:3]): cls._create_val(line) for line in my_str.split("\n")},
        )

    @classmethod
    def _create_val(cls, line: str) -> Direction:
        key, left, right = re.compile(r"\w{3}").findall(
            line
        )  # assumes Nodes are three characters
        return Direction(Node(left), Node(right))

    def go_next_location(self, inst: Instruction) -> None:
        self.current_loc = self.dirs[self.current_loc].get_next_loc(inst)
        logger.debug(f"Current Location: {self.current_loc}")


def parse_input(
    file_path: Path = Path("./input/input.txt"),
) -> tuple[list[Instruction], Map]:
    # First make grid
    with open(file_path, "r") as file:
        insts = [
            Instruction.LEFT if c == "L" else Instruction.RIGHT
            for c in file.readline().strip()
        ]  # read first line
        file.readline()  # read empty line
        my_map = Map.from_str(file.read())  # read remainder of file

    return insts, my_map
