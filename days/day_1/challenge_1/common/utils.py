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
        """Extract first and last digits from raw string and combine them into a two-digit number."""
        digits = [char for char in self.raw if char.isdigit()]
        if not digits:
            logger.warning(f"No digits found in input string: {self.raw}")
            return 0
        return int(digits[0] + digits[-1])


def parse_input(file_path: Path = Path("./input/input.txt")) -> list[Calibration]:
    """Parse input file and return list of Calibration objects.

    Args:
        file_path: Path to input file containing calibration values

    Returns:
        List of Calibration objects parsed from input file
    """
    try:
        with open(file_path) as f:
            reader = csv.reader(f)
            data = [Calibration(row[0]) for row in reader]
        return data
    except FileNotFoundError:
        logger.error(f"Input file not found: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Error parsing input file: {e}")
        return []
