from pathlib import Path
from dataclasses import dataclass
import logging
from scipy.spatial.distance import pdist
import scipy.sparse as sps
import numpy as np
import numpy.typing as npt

logger = logging.getLogger(__name__)
NDArrayInt = npt.NDArray[np.int_]


@dataclass
class Image:
    universe: NDArrayInt

    @property
    def galaxy_coords(self) -> NDArrayInt:
        return np.array(self.universe.nonzero()).transpose()

    @classmethod
    def from_str(cls, input: str):
        """Convert . to 0, convert # to 1, create numpy array"""
        return cls(
            sps.csc_matrix(
                np.array(
                    [
                        row[:-1].split(",")
                        for row in input.replace(".", "0,")
                        .replace("#", "1,")
                        .split("\n")
                    ]
                ).astype(int),
                dtype=int,
            )
        )

    def expand_universe(self) -> None:
        self._expand_rows()
        self._expand_cols()

    def _expand_rows(self):
        for rid in range(self.universe.shape[0]):
            if rid == 0:
                if self.universe[rid, :].count_nonzero() > 0:
                    # initialize matrix with first row
                    new_matrix = self.universe[rid, :]
                else:
                    # initialize matrix with 1 mil rows
                    new_matrix = sps.csc_matrix(
                        (1000000, self.universe[rid, :].shape[1])
                    )
            else:
                if self.universe[rid, :].count_nonzero() > 0:
                    # add this row
                    new_matrix = sps.vstack([new_matrix, self.universe[rid, :]])
                else:
                    # add million rows
                    new_matrix = sps.vstack(
                        [
                            new_matrix,
                            sps.csc_matrix((1000000, self.universe[rid, :].shape[1])),
                        ]
                    )
        self.universe = new_matrix

    def _expand_cols(self):
        for cid in range(self.universe.shape[1]):
            if cid == 0:
                if self.universe[:, cid].count_nonzero() > 0:
                    # initialize matrix with first col
                    new_matrix = self.universe[:, cid]
                else:
                    # initialize matrix with 1 mil rows
                    new_matrix = sps.csc_matrix(
                        (self.universe[:, cid].shape[0], 1000000)
                    )
            else:
                if self.universe[:, cid].count_nonzero() > 0:
                    # add this row
                    new_matrix = sps.hstack([new_matrix, self.universe[:, cid]])
                else:
                    # add million rows
                    new_matrix = sps.hstack(
                        [
                            new_matrix,
                            sps.csc_matrix((self.universe[:, cid].shape[0], 1000000)),
                        ]
                    )
        self.universe = new_matrix

    def get_sum_shortest_distance(self) -> int:
        return pdist(self.galaxy_coords, metric="cityblock").sum()


def parse_input(file_path: Path = Path("./input/input.txt")) -> None:
    # First make grid
    with open(file_path, "r") as file:
        full_text = file.read()
        image = Image.from_str(full_text)
        image.expand_universe()
        logger.info(f"****Answer: {image.get_sum_shortest_distance()}****")
