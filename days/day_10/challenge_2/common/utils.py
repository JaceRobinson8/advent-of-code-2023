from pathlib import Path
from dataclasses import dataclass
import logging
from enum import StrEnum, auto
from typing import NamedTuple

logger = logging.getLogger(__name__)


class Loc(NamedTuple):
    """1 based location indexing into Grid"""

    row: int
    col: int

    def __str__(self):
        return f"({self.row},{self.col})"

    def __repr__(self):
        return f"({self.row},{self.col})"


class Dirs(StrEnum):
    N = auto()
    S = auto()
    E = auto()
    W = auto()

    @classmethod
    def flip(cls, in_dir):
        match in_dir:
            case cls.N:
                out_dir = cls.S
            case cls.S:
                out_dir = cls.N
            case cls.E:
                out_dir = cls.W
            case cls.W:
                out_dir = cls.E
        return out_dir


class PipeTypes(StrEnum):
    NS = "|"
    EW = "-"
    NE = "L"
    NW = "J"
    SW = "7"
    SE = "F"
    G = "."
    S = "S"  # watch this doesn't conflict with south


@dataclass
class Tile:
    """Single entry in the grid"""

    ptype: PipeTypes
    in_loop: bool = False
    is_vert: bool = False

    @classmethod
    def from_str(cls, char: str):
        ptype = PipeTypes(char)
        is_vert = False
        if ptype == PipeTypes.NS:
            is_vert = True
        return cls(ptype=ptype, is_vert=is_vert)

    def __str__(self):
        return self.ptype.value

    def __repr__(self):
        return self.ptype.value

    @property
    def dir(self) -> tuple[Dirs, Dirs] | None:
        match self.ptype:
            case PipeTypes.NS:
                dirs = (Dirs.N, Dirs.S)
            case PipeTypes.EW:
                dirs = (Dirs.E, Dirs.W)
            case PipeTypes.NE:
                dirs = (Dirs.N, Dirs.E)
            case PipeTypes.NW:
                dirs = (Dirs.N, Dirs.W)
            case PipeTypes.SW:
                dirs = (Dirs.S, Dirs.W)
            case PipeTypes.SE:
                dirs = (Dirs.S, Dirs.E)
            case _:
                dirs = None
        return dirs

    def check_valid(self, dir: Dirs) -> bool:
        """Given a direction, check if the provided direction in self.dir"""
        return bool(self.dir) and (dir in self.dir)

    def get_next_dir(self, prev_dir: Dirs) -> Dirs:
        # Return the other dir
        if self.dir[0] == prev_dir:
            return self.dir[1]
        else:
            return self.dir[0]


def check_north(t1: Tile, t2: Tile) -> bool:
    """Return True if tile1 connects to tile2 north, else False."""
    res = False
    if t1.ptype == PipeTypes.NS:
        if Dirs.S in t2.directions:
            res = True
    elif t1.ptype == PipeTypes.EW:
        pass
    # LEAVING OFF HERE... THINK A BIT MORE FOR A BETTER SOLUTION...

    return res


@dataclass
class Grid:
    g: list[list[Tile]]
    n_rows: int
    n_cols: int
    sloc: Loc  # starting location
    cloc: Loc  # current location
    pdir: Dirs  # previous direction

    @classmethod
    def from_str(cls, input_text: str):
        loc = Loc(-1, -1)
        grid = []
        for rid, row in enumerate(input_text.split("\n")):
            new_row = []
            for cid, col in enumerate(row):
                new_row.append(Tile.from_str(col))
                if col == PipeTypes.S.value:
                    loc = Loc(rid, cid)
            grid.append(new_row)

        # grid = [[Tile.from_str(col) for col in row] for row in input_text.split("\n")]
        return cls(
            g=grid,
            n_rows=len(grid),
            n_cols=len(grid[0]),
            sloc=loc,
            cloc=Loc(loc.row, loc.col),
            pdir=None,
        )

    def get(self, loc: Loc) -> Tile:
        return self.g[loc.row][loc.col]

    def new_loc(self, loc: Loc, direction: Dirs) -> Loc:
        match direction:
            case Dirs.N:
                new_loc = Loc(loc.row - 1, loc.col)
            case Dirs.S:
                new_loc = Loc(loc.row + 1, loc.col)
            case Dirs.E:
                new_loc = Loc(loc.row, loc.col + 1)
            case Dirs.W:
                new_loc = Loc(loc.row, loc.col - 1)
            case _:
                raise ValueError("unexpection direction")
        return new_loc

    def update_start_tile(self) -> None:
        """Replace start tile from S to real pipe"""
        dirs = [Dirs.N, Dirs.S, Dirs.E, Dirs.W]
        # Check all four directions until you find valid, then traverse it
        valid_state = []
        for dir in dirs:
            new_loc = self.new_loc(loc=self.cloc, direction=dir)
            tile = self.get(new_loc)
            valid_state.append(tile.check_valid(Dirs.flip(dir)))
            # STOPPING HERE
        pass

    def traverse_path(self) -> int:
        # From current location
        # 1. check north
        # 2. check east
        # 3. check south
        # 4. check west
        # don't move to previous location
        path_length = 0
        start_tile = self.get(self.sloc)
        start_tile.in_loop = True
        self.update_start_tile()

        ### Special first case
        dirs = [Dirs.N, Dirs.S, Dirs.E, Dirs.W]
        # Check all four directions until you find valid, then traverse it
        for dir in dirs:
            new_loc = self.new_loc(loc=self.cloc, direction=dir)
            tile = self.get(new_loc)
            # flip dir to indicate where you came from
            if tile.check_valid(Dirs.flip(dir)):
                self.cloc = new_loc
                self.pdir = dir
                path_length += 1
                break  # no need to check rest of directions

        while self.cloc != self.sloc:
            # Use previous location to determine next location
            current_tile = self.get(self.cloc)
            current_tile.in_loop = True
            # advance direction
            self.pdir = current_tile.get_next_dir(Dirs.flip(self.pdir))
            # advance location
            self.cloc = self.new_loc(loc=self.cloc, direction=self.pdir)
            path_length += 1

        return path_length / 2

    def count_enclosed(self) -> int:
        # For each row, count number of intersections with pipe from this tile to right end.
        # If even, this means outside
        # If odd, this means inside.
        # From ray casting algorithm https://en.wikipedia.org/wiki/Point_in_polygon#:~:text=One%20simple%20way%20of%20finding,an%20even%20number%20of%20times.
        # To determine if any point is in a polygon
        count = 0
        for row in range(self.n_rows):
            for col in range(self.n_cols):
                intersect_count = 0
                if not self.g[row][col].in_loop:  # skip elements that are in loop
                    for col2 in range(
                        col + 1, self.n_cols
                    ):  # check from this position to the end
                        if self.g[row][col2].in_loop and self.g[row][col2].is_vert:
                            intersect_count += 1
                    if intersect_count % 2 == 1:  # found a tile in loop
                        count += 1
        return count


def parse_input(file_path: Path = Path("./input/input.txt")) -> None:
    # First make grid
    with open(file_path, "r") as file:
        g = Grid.from_str(file.read())
        path_count = g.traverse_path()
        logger.info(f"****Answer: {g.count_enclosed()}****")
    return g
