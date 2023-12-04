from pathlib import Path
import csv
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class Calibration:
    raw: str

    @property
    def cal_val(self) -> int:
        logger.debug("Raw: %s", self.raw)
        self._replace_words()
        digits = [char for char in self.raw if char.isdigit()]
        cal_val = int(digits[0] + digits[-1])
        logger.debug("Modified Raw: %s", self.raw)
        logger.debug("Calibration: %d", cal_val)
        return cal_val

    def _replace_words(self):
        # Special case "eightwothree"
        # By appending first and last character of each word to numeric value,
        # this will handle overlapping words like the above special case.
        self.raw = (
            self.raw.replace("one", "o1e")
            .replace("two", "t2o")
            .replace("three", "t3e")
            .replace("four", "f4r")
            .replace("five", "f5e")
            .replace("six", "s6x")
            .replace("seven", "s7n")
            .replace("eight", "e8t")
            .replace("nine", "n9e")
        )


def parse_input(file_path: Path = Path("./input/input.txt")) -> list[Calibration]:
    with open(file_path) as f:
        reader = csv.reader(f)
        data = [Calibration(row[0]) for row in reader]
    return data
