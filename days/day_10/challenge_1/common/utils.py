from pathlib import Path
from dataclasses import dataclass
import logging
from enum import Enum

logger = logging.getLogger(__name__)



class PipeTypes(Enum):
    NS = "|"
    EW = "-"
    NE = "L"
    NW = "J"
    SW = "7"
    SE = "F"
    G = "."
    S = "S"

class Dirs(Enum):
    N = "N"
    S = "S"
    E = "E"
    W = "W"


@dataclass
class Tile:
    """Single entry in the grid"""

    ptype: PipeTypes

    @classmethod
    def from_str(cls, char: str):
        if char == PipeTypes.NS.value:
            my_tile = cls(PipeTypes.NS)
        elif char == PipeTypes.EW.value:
            my_tile = cls(PipeTypes.EW)
        elif char == PipeTypes.NE.value:
            my_tile = cls(PipeTypes.NE)
        elif char == PipeTypes.NW.value:
            my_tile = cls(PipeTypes.NW)
        elif char == PipeTypes.SE.value:
            my_tile = cls(PipeTypes.SE)
        elif char == PipeTypes.SW.value:
            my_tile = cls(PipeTypes.SW)
        elif char == PipeTypes.G.value:
            my_tile = cls(PipeTypes.G)
        elif char == PipeTypes.S.value:
            my_tile = cls(PipeTypes.S)
        else:
            raise ValueError("Unexpected Tile")
        return my_tile

    def __str__(self):
        return self.ptype.value

    def __repr__(self):
        return self.ptype.value
    
    @property
    def directions(self) -> list[Dirs, Dirs]:
        """Return two directions"""
        if self.ptype == PipeTypes.NS:
            return [Dirs.N, Dirs.S]
        elif self.ptype == PipeTypes.EW:
            return [Dirs.E, Dirs.W]
        elif self.ptype == PipeTypes.NE:
            return [Dirs.N, Dirs.E]
        elif self.ptype == PipeTypes.NW:
            return [Dirs.N, Dirs.W]
        elif self.ptype == PipeTypes.SE:
            return [Dirs.S, Dirs.E]
        elif self.ptype == PipeTypes.SW:
            return [Dirs.S, Dirs.W]
    
        



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
    sloc: tuple[int, int]  # starting location
    cloc: tuple[int, int]  # current location
    ploc: tuple[int, int]  # previous location

    @classmethod
    def from_str(cls, input_text: str):
        loc = (-1, -1)
        grid = []
        for rid, row in enumerate(input_text.split("\n")):
            new_row = []
            for cid, col in enumerate(row):
                new_row.append(Tile.from_str(col))
                if col == PipeTypes.S.value:
                    loc = (rid, cid)
            grid.append(new_row)

        # grid = [[Tile.from_str(col) for col in row] for row in input_text.split("\n")]
        return cls(
            g=grid, n_rows=len(grid), n_cols=len(grid[0]), sloc=loc, cloc=loc, ploc=loc
        )


    def go_next_location(self, first_iter=False):
        # From current location
        # 1. check north
        # 2. check east
        # 3. check south
        # 4. check west
        # don't move to previous location


        
        
        
        if first_iter: # don't update previous location



def parse_input(file_path: Path = Path("./input/input.txt")) -> None:
    # First make grid
    with open(file_path, "r") as file:
        g = Grid.from_str(file.read())
        g.go_next_location(first_iter=True)
        logger.debug(f"cloc: {g.cloc}")
        logger.debug(f"ploc: {g.ploc}")
        g.go_next_location(first_iter=False)
        logger.debug(f"cloc: {g.cloc}")
        logger.debug(f"ploc: {g.ploc}")
        logger.debug(g)
    return g
