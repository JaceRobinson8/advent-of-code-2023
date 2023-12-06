from pathlib import Path
from dataclasses import dataclass
import logging
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class PartNumber:
    # Index rows and columns of grid
    # Each part number is on a single row, spans multiple columns from start to end (inclusive)
    row_index: int
    col_index_start: int
    col_index_end: int
    number: int


@dataclass
class Grid:
    g: np.chararray

    @classmethod
    def from_str(cls, grid_str: str):
        lines = grid_str.split("\n")
        num_rows = len(lines)
        num_cols = len(lines[0])
        g = np.chararray((num_rows, num_cols))
        for r in range(num_rows):
            for c in range(num_rows):
                g[r, c] = lines[r][c]
        return cls(g)

    @property
    def n_row(self) -> int:
        return self.g.shape[0]

    @property
    def n_col(self) -> int:
        return self.g.shape[1]

    def get_part_numbers(self) -> list[PartNumber]:
        # Loop over the grid, looking for part numbers
        # (continuous blocks of numbers in a row)
        part_numbers = []
        for r in range(self.n_row):
            found_part = False
            col_start = -1
            col_end = -1
            for c in range(self.n_col):
                # logger.debug(f"({r},{c})")
                if self.g[r, c].isdigit():
                    col_end = c
                    if not found_part:  # we found start of new number
                        found_part = True
                        col_start = c
                else:
                    if found_part:  #
                        part_numbers.append(
                            PartNumber(
                                r,
                                col_start,
                                col_end,
                                int(
                                    "".join(
                                        self.g[r, col_start : (col_end + 1)].astype(str)
                                    )
                                ),
                            )
                        )
                        found_part = False
            if found_part:  #
                part_numbers.append(
                    PartNumber(
                        r,
                        col_start,
                        col_end,
                        int("".join(self.g[r, col_start : (col_end + 1)].astype(str))),
                    )
                )
        return part_numbers

    def validate_part(self, part: PartNumber) -> bool:
        valid_part = False  # false until a symbol found, then true
        if part.col_index_start == 0:
            col_start = part.col_index_start
        else:
            col_start = part.col_index_start - 1
        if part.col_index_end + 1 == self.n_col:
            col_end = part.col_index_end
        else:
            col_end = part.col_index_end + 1

        logger.debug(part)

        # check row above
        valid_part = valid_part or self.check_above(part.row_index, col_start, col_end)
        # check row below
        valid_part = valid_part or self.check_below(part.row_index, col_start, col_end)
        # check left
        valid_part = valid_part or self.check_left(part.row_index, part.col_index_start)
        # check right
        # valid_part = valid_part or self.check_right(part.row_index, part.col_index_end)
        valid_part = self.check_right(part.row_index, part.col_index_end) or valid_part

        return valid_part

    def check_above(self, row: int, col_start: int, col_end: int) -> bool:
        condition = False
        if row > 0:
            condition = self.check(
                self.g[
                    row - 1,
                    col_start : (col_end + 1),
                ]
            )
        return condition

    def check_below(self, row: int, col_start: int, col_end: int) -> bool:
        condition = False
        if row + 1 < self.n_row:
            condition = self.check(
                self.g[
                    row + 1,
                    col_start : (col_end + 1),
                ]
            )
        return condition

    def check_left(self, row: int, col_start: int) -> bool:
        condition = False
        if col_start > 0:
            condition = self.check(
                self.g[
                    row,
                    col_start - 1,
                ]
            )
        return condition

    def check_right(self, row: int, col_end: int) -> bool:
        condition = False
        if col_end + 1 < self.n_col:
            condition = self.check(
                self.g[
                    row,
                    col_end + 1,
                ]
            )
        return condition

    def check(self, char_array: np.chararray) -> bool:
        if len(char_array) > 1:
            condition = any(
                [(not val.isdigit()) and (val != ".") for val in char_array.astype(str)]
            )
        else:
            val = char_array.decode()
            condition = (not val.isdigit()) and (val != ".")
        return condition


def parse_input(file_path: Path = Path("./input/input.txt")):
    # First make grid
    with open(file_path, "r") as file:
        grid = Grid.from_str(file.read())
    logger.debug("Grid:")
    logger.debug(grid.g)

    part_numbers = grid.get_part_numbers()
    logger.debug("Part_numbers:")
    [logger.debug(part_number.number) for part_number in part_numbers]
    logger.debug(f"Number of parts: {len(part_numbers)}")
    logger.debug("Validations:")
    logger.debug([grid.validate_part(p) for p in part_numbers])
    logger.debug(sum([p.number for p in part_numbers if grid.validate_part(p)]))

    return None
