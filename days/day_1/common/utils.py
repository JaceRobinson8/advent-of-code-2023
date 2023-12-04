from pathlib import Path
import csv


class Calibration:
    pass


def parse_input(file_path: Path = Path("./input/input.txt")):
    with open(file_path) as f:
        reader = csv.reader(f)
        data = list(reader)

    return data
