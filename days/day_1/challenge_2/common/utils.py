from pathlib import Path
import csv
from dataclasses import dataclass
import logging
import re


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

    @property
    def cal_val_regex(self) -> int:
        # Use regex instead of string replacement! Use regex to find:
        # 1. First match forwards string
        # 2. Last match (as first match in reversed string)
        logger.debug("Raw: %s", self.raw)
        cal_val = int(self._first_digit() + self._last_digit())
        logger.debug("Calibration: %d", cal_val)
        return cal_val

    def _first_digit(self) -> str:
        # Search for numeric or word version in string, find FIRST match
        regex = r"[0-9]|one|two|three|four|five|six|seven|eight|nine"
        matches = re.search(regex, self.raw)
        return self._convert(matches.group())

    def _last_digit(self) -> str:
        # Search for numeric or word version in REVERSED string, find FIRST match
        # Reverse names of words
        regex = r"[0-9]|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin"
        matches = re.search(regex, "".join(reversed(self.raw)))
        return self._convert(matches.group())

    def _convert(self, s: str) -> str:
        if s == "one" or s == "eno":
            return "1"
        elif s == "two" or s == "owt":
            return "2"
        elif s == "three" or s == "eerht":
            return "3"
        elif s == "four" or s == "ruof":
            return "4"
        elif s == "five" or s == "evif":
            return "5"
        elif s == "six" or s == "xis":
            return "6"
        elif s == "seven" or s == "neves":
            return "7"
        elif s == "eight" or s == "thgie":
            return "8"
        elif s == "nine" or s == "enin":
            return "9"
        else:
            return s


def parse_input(file_path: Path = Path("./input/input.txt")) -> list[Calibration]:
    with open(file_path) as f:
        reader = csv.reader(f)
        data = [Calibration(row[0]) for row in reader]
    return data
