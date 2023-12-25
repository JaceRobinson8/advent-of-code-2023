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

    def clip(self, val: int, ub: int, lb: int = 0) -> int:
        return max(
            lb,
            min(ub - 1, val),
        )

    def get(self, rid: int, cid: int | range) -> str:
        if isinstance(cid, int):  # cid is single index
            return self.g[self.clip(rid, len(self.g))][self.clip(cid, len(self.g[0]))]
        else:  # cid is range of index
            return "".join(
                [
                    self.g[self.clip(rid, len(self.g))][self.clip(c, len(self.g[0]))]
                    for c in cid
                ]
            )

    def validate_part(self, part: PartNumber) -> bool:
        return (
            self.check_left(part)
            or self.check_right(part)
            or self.check_above(part)
            or self.check_below(part)
        )

    def check_left(self, part: PartNumber) -> bool:
        return self.check(self.get(part.row_index, part.col_index_start - 1))

    def check_right(self, part: PartNumber) -> bool:
        return self.check(self.get(part.row_index, part.col_index_end))

    def check_above(self, part: PartNumber) -> bool:
        return self.check(
            self.get(
                part.row_index - 1,
                range(part.col_index_start - 1, part.col_index_end + 1),
            )
        )

    def check_below(self, part: PartNumber) -> bool:
        return self.check(
            self.get(
                part.row_index + 1,
                range(part.col_index_start - 1, part.col_index_end + 1),
            )
        )

    def check(self, val: str) -> bool:
        if len(val) > 1:
            res = any([(not x.isdigit()) and (x != ".") for x in val])
        else:
            res = (not val.isdigit()) and (val != ".")
        return res


def parse_input(file_path: Path = Path("./input/input.txt")) -> list[PartNumber]:
    # First make grid
    with open(file_path, "r") as file:
        grid = Grid.from_str(file.read())
    part_numbers = grid.get_part_numbers()
    logger.debug(f"Number of parts: {len(part_numbers)}")
    logger.debug("Validations:")
    logger.debug([grid.validate_part(p) for p in part_numbers])
    logger.info(
        f"****Answer: {sum([p.number for p in part_numbers if grid.validate_part(p)])}****"
    )
    return None
