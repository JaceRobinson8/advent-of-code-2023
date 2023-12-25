from pathlib import Path
from dataclasses import dataclass
import logging
import numpy as np
import re

logger = logging.getLogger(__name__)


@dataclass
class PartNumber:
    # Index rows and columns of grid
    # Each part number is on a single row, spans multiple columns from start to end (inclusive)
    row_index: int
    col_index_start: int
    col_index_end: int
    number: int
    valid: bool = False


@dataclass
class Grid:
    g: list[str]

    @classmethod
    def from_str(cls, grid_str: str):
        return cls(grid_str.split("\n"))

    @property
    def n_row(self) -> int:
        return len(self.g)

    @property
    def n_col(self) -> int:
        return len(self.g[0])

    def get_part_numbers(self) -> list[PartNumber]:
        partNumbers = []
        for id, line in enumerate(self.g):
            for match in re.finditer(r"\d+", line):
                partNumbers.append(
                    PartNumber(
                        row_index=id,
                        col_index_start=match.start(),
                        col_index_end=match.end(),
                        number=int(match.group()),
                    )
                )
        return partNumbers

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

    def validate_part2(self, part: PartNumber) -> bool:
        return (
            self.check_left2(part)
            or self.check_right2(part)
            or self.check_above2(part)
            or self.check_below2(part)
        )

    def check_left2(self, part: PartNumber) -> bool:
        val = self.g[part.row_index][max(0, part.col_index_start - 1)]
        return (not val.isdigit()) and (val != ".")

    def check_right2(self, part: PartNumber) -> bool:
        val = self.g[part.row_index][
            min(len(self.g[part.row_index]) - 1, part.col_index_end)
        ]
        return (not val.isdigit()) and (val != ".")

    def check_above2(self, part: PartNumber) -> bool:
        val = self.g[part.row_index][
            min(len(self.g[part.row_index]) - 1, part.col_index_end)
        ]
        return (not val.isdigit()) and (val != ".")


def parse_input(file_path: Path = Path("./input/input.txt")) -> list[PartNumber]:
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
    logger.debug([grid.validate_part2(p) for p in part_numbers])
    logger.debug(sum([p.number for p in part_numbers if grid.validate_part(p)]))

    return None
