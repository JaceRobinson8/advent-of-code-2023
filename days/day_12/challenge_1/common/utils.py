from pathlib import Path
from dataclasses import dataclass, field
import logging
from scipy.spatial.distance import pdist, squareform
import numpy as np
import numpy.typing as npt


def parse_input(file_path: Path = Path("./input/input.txt")) -> None:
    # First make grid
    with open(file_path, "r") as file:
        full_text = file.read()
