from pathlib import Path
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class Map:
    dest_starts: list[int] = field(default_factory=list)
    src_starts: list[int] = field(default_factory=list)
    lengths: list[int] = field(default_factory=list)

    def get(self, idx: int) -> int:
        out_idx = idx  # default value if idx not in any ranges
        for i in range(len(self.src_starts)):
            if (idx >= self.src_starts[i]) and idx < (
                self.src_starts[i] + self.lengths[i]
            ):
                diff = (
                    idx - self.src_starts[i]
                )  # get different in source, and use that to map to dest
                out_idx = self.dest_starts[i] + diff
                break  # early terminate
        return out_idx

    def append(self, dest_start: int, src_start: int, length: int) -> None:
        self.dest_starts.append(dest_start)
        self.src_starts.append(src_start)
        self.lengths.append(length)


@dataclass
class Almanac:
    seed2soil: Map = field(default_factory=Map)
    soil2fert: Map = field(default_factory=Map)
    fert2water: Map = field(default_factory=Map)
    water2light: Map = field(default_factory=Map)
    light2temp: Map = field(default_factory=Map)
    temp2hum: Map = field(default_factory=Map)
    hum2loc: Map = field(default_factory=Map)

    @classmethod
    def build_maps(cls, pages: list[str]):
        almanac = cls()
        [almanac.build_single_map(page) for page in pages]
        return almanac

    def build_single_map(self, page: str) -> None:
        title, content = page.split(":\n")
        for line in content.split("\n"):
            dest_start, src_start, length = line.split(" ")
            self.update_map(
                dict_name=title,
                dest_start=int(dest_start),
                src_start=int(src_start),
                length=int(length),
            )

    def update_map(self, dict_name: str, dest_start: int, src_start: int, length: int):
        if dict_name == "seed-to-soil map":
            my_map = self.seed2soil
        elif dict_name == "soil-to-fertilizer map":
            my_map = self.soil2fert
        elif dict_name == "fertilizer-to-water map":
            my_map = self.fert2water
        elif dict_name == "water-to-light map":
            my_map = self.water2light
        elif dict_name == "light-to-temperature map":
            my_map = self.light2temp
        elif dict_name == "temperature-to-humidity map":
            my_map = self.temp2hum
        elif dict_name == "humidity-to-location map":
            my_map = self.hum2loc
        else:
            raise KeyError("Unexpected map name")

        my_map.append(dest_start, src_start, length)

    def get_location(self, seed: int) -> int:
        logger.debug(f"seed: {seed}")
        soil = self.seed2soil.get(seed)
        logger.debug(f"soil: {soil}")
        fert = self.soil2fert.get(soil)
        logger.debug(f"fert: {fert}")
        water = self.fert2water.get(fert)
        logger.debug(f"water: {water}")
        light = self.water2light.get(water)
        logger.debug(f"light: {light}")
        temp = self.light2temp.get(light)
        logger.debug(f"temp: {temp}")
        hum = self.temp2hum.get(temp)
        logger.debug(f"hum: {hum}")
        loc = self.hum2loc.get(hum)
        logger.debug(f"loc: {loc}")
        return loc


def parse_input(file_path: Path = Path("./input/input.txt")) -> None:
    # First make grid
    with open(file_path, "r") as file:
        full_text = file.read()
        pages = full_text.split("\n\n")
        seed_nums = pages[0].split("seeds:")[1].strip().split(" ")
        my_almanac = Almanac.build_maps(pages[1:])

    score = min([my_almanac.get_location(int(seed)) for seed in seed_nums])
    logger.info("****Answer:****")
    logger.info(score)
    return None
