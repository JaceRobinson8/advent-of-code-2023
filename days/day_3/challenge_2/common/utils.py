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
class Gear:
    row_index: int  # row id
    col_index_start: int  # cid
    col_index_end: int
    valid: bool = False
    ratio: int = 0


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

    def get_gears(self) -> list[Gear]:
        gears = []
        for id, line in enumerate(self.g):
            for match in re.finditer(r"\*", line):
                gears.append(
                    Gear(
                        row_index=id,
                        col_index_start=match.start(),
                        col_index_end=match.end(),
                    )
                )
        return gears

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

    def get_gear_ratio(self, gear: Gear, parts: list[PartNumber]) -> None:
        found_parts: list[PartNumber] = []

        # left
        found_parts.extend(
            self.find_part_number_val(parts, gear.row_index, gear.col_index_start - 1)
        )
        # right
        found_parts.extend(
            self.find_part_number_val(parts, gear.row_index, gear.col_index_start + 1)
        )
        # above
        found_parts.extend(
            self.find_part_number_val(
                parts,
                gear.row_index - 1,
                range(gear.col_index_start - 1, gear.col_index_end + 1),
            )
        )
        # below
        found_parts.extend(
            self.find_part_number_val(
                parts,
                gear.row_index + 1,
                range(gear.col_index_start - 1, gear.col_index_end + 1),
            )
        )

        if len(found_parts) == 2:  # exactly 2 parts
            gear.ratio = found_parts[0].number * found_parts[1].number
            gear.valid = True

    def find_part_number_val(
        self, parts: list[PartNumber], rid: int, cid: int
    ) -> list[PartNumber]:
        found_parts = []
        if isinstance(cid, range):  # could match multiple parts
            cmin = cid[0]
            cmiddle = cid[1]
            cmax = cid[-1]
            for p in parts:
                if (
                    p.row_index == rid
                    and cmin >= p.col_index_start
                    and cmin < p.col_index_end
                ):
                    found_parts.append(p)
                elif (
                    p.row_index == rid
                    and cmax >= p.col_index_start
                    and cmax < p.col_index_end
                ):
                    found_parts.append(p)
                elif (
                    p.row_index == rid
                    and cmiddle >= p.col_index_start
                    and cmiddle < p.col_index_end
                ):
                    found_parts.append(p)

        else:
            for p in parts:
                if (
                    p.row_index == rid
                    and cid >= p.col_index_start
                    and cid < p.col_index_end
                ):
                    found_parts.append(p)
                    break
        return found_parts

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
            res = any([x.isdigit() for x in val])
        else:
            res = val.isdigit()
        return res


def parse_input(file_path: Path = Path("./input/input.txt")) -> list[PartNumber]:
    # First make grid
    with open(file_path, "r") as file:
        grid = Grid.from_str(file.read())
    part_numbers = grid.get_part_numbers()
    gears = grid.get_gears()
    logger.debug(f"Number of gears: {len(gears)}")
    logger.debug("Validations:")
    [grid.get_gear_ratio(g, part_numbers) for g in gears]
    logger.info(f"****Answer: {sum([g.ratio for g in gears if g.valid])}****")
    return None
