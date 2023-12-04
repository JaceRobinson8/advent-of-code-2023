from pathlib import Path
import csv
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


# @dataclass
# class Calibration:
#     raw: str

#     @property
#     def cal_val(self) -> int:
#         digits = [char for char in self.raw if char.isdigit()]
#         return int(digits[0] + digits[-1])


# def parse_input(file_path: Path = Path("./input/input.txt")) -> list[Calibration]:
#     with open(file_path) as f:
#         reader = csv.reader(f)
#         data = [Calibration(row[0]) for row in reader]
#     return data
