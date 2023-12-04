from pathlib import Path
import csv
from dataclasses import dataclass
import logging

logger = logging


@dataclass
class Calibration:
    raw_string: str

    @property
    def calibration_value(self) -> int:
        first = "0"
        last = "0"
        first_digit = True
        for id_inner, val_inner in enumerate(self.raw_string):
            if val_inner.isdigit():
                if first_digit:
                    first = val_inner
                    first_digit = False
                last = val_inner
        return int(first + last)


def parse_input(file_path: Path = Path("./input/input.txt")) -> list[Calibration]:
    with open(file_path) as f:
        reader = csv.reader(f)
        data = [Calibration(row[0]) for row in reader]
    return data
