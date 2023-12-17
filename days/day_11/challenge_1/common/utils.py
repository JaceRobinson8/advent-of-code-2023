from pathlib import Path
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


def parse_input(file_path: Path = Path("./input/input.txt")) -> None:
    # First make grid
    with open(file_path, "r") as file:
        full_text = file.read()

    return None
