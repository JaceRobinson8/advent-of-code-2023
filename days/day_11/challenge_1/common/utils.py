from pathlib import Path
from dataclasses import dataclass, field
import logging
from scipy.spatial.distance import pdist, squareform
import numpy as np
import numpy.typing as npt

logger = logging.getLogger(__name__)
NDArrayInt = npt.NDArray[np.int_]


@dataclass
class Image:
    universe: NDArrayInt

    @property
    def galaxy_coords(self) -> NDArrayInt:
        return np.array(np.where(self.universe != 0)).transpose()

    @classmethod
    def from_str(cls, input: str):
        """Convert . to 0, convert # to 1, create numpy array"""
        return cls(
            np.array(
                [
                    row[:-1].split(",")
                    for row in input.replace(".", "0,").replace("#", "1,").split("\n")
                ]
            ).astype(int)
        )

    def expand_universe(self) -> None:
        # Get column indices with all zero elements
        cols_to_expand = np.where(self.universe.sum(axis=0) == 0)[0].tolist()
        # Add column indices to exist indicies to duplicate the row
        col_indices = list(range(self.universe.shape[1]))
        col_indices.extend(cols_to_expand)
        col_indices.sort()
        self.universe = self.universe[:, col_indices]
        # Get row indices with all zero elements
        rows_to_expand = np.where(self.universe.sum(axis=1) == 0)[0].tolist()
        # Add row indices to exist indicies to duplicate the row
        row_indices = list(range(self.universe.shape[0]))
        row_indices.extend(rows_to_expand)
        row_indices.sort()
        self.universe = self.universe[row_indices, :]

    def get_sum_shortest_distance(self) -> float:
        return pdist(self.galaxy_coords, metric="cityblock").sum()


def parse_input(file_path: Path = Path("./input/input.txt")) -> None:
    # First make grid
    with open(file_path, "r") as file:
        full_text = file.read()
        image = Image.from_str(full_text)
        image.expand_universe()
        logger.info(f"****Answer: {image.get_sum_shortest_distance()}****")
