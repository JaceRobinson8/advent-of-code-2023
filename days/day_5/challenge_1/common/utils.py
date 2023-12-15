from pathlib import Path
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class Almanac:
    seed2soil: dict = field(default_factory=dict)
    soil2fert: dict = field(default_factory=dict)
    fert2water: dict = field(default_factory=dict)
    water2light: dict = field(default_factory=dict)
    light2temp: dict = field(default_factory=dict)
    temp2hum: dict = field(default_factory=dict)
    hum2loc: dict = field(default_factory=dict)

    @classmethod
    def build_maps(cls, pages: list[str]):
        almanac = cls()
        [almanac.build_single_map(page) for page in pages]
        return almanac

    def build_single_map(self, page: str) -> None:
        title, content = page.split(":\n")
        for line in content.split("\n"):
            dest_start, src_start, length = line.split(" ")
            self.update_dict(
                dict_name=title,
                dest_start=int(dest_start),
                src_start=int(src_start),
                length=int(length),
            )

    def update_dict(self, dict_name: str, dest_start: int, src_start: int, length: int):
        if dict_name == "seed-to-soil map":
            my_dict = self.seed2soil
        elif dict_name == "soil-to-fertilizer map":
            my_dict = self.soil2fert
        elif dict_name == "fertilizer-to-water map":
            my_dict = self.fert2water
        elif dict_name == "water-to-light map":
            my_dict = self.water2light
        elif dict_name == "light-to-temperature map":
            my_dict = self.light2temp
        elif dict_name == "temperature-to-humidity map":
            my_dict = self.temp2hum
        elif dict_name == "humidity-to-location map":
            my_dict = self.hum2loc
        else:
            raise KeyError("Unexpected map name")

        my_dict.update(
            dict(
                zip(
                    range(src_start, src_start + length),
                    range(dest_start, dest_start + length),
                )
            )
        )

    def get_location(self, seed: int) -> int:
        logger.debug(f"seed: {seed}")
        soil = self.seed2soil.get(seed, seed)
        logger.debug(f"soil: {soil}")
        fert = self.soil2fert.get(soil, soil)
        logger.debug(f"fert: {fert}")
        water = self.fert2water.get(fert, fert)
        logger.debug(f"water: {water}")
        light = self.water2light.get(water, water)
        logger.debug(f"light: {light}")
        temp = self.light2temp.get(light, light)
        logger.debug(f"temp: {temp}")
        hum = self.temp2hum.get(temp, temp)
        logger.debug(f"hum: {hum}")
        loc = self.hum2loc.get(hum, hum)
        logger.debug(f"loc: {loc}")
        return loc


def parse_input(file_path: Path = Path("./input/input.txt")) -> None:
    # First make grid
    with open(file_path, "r") as file:
        full_text = file.read()
        pages = full_text.split("\n\n")
        seed_line = pages[0]
        seed_nums = seed_line.split("seeds:")[1].strip().split(" ")
        my_alamac = Almanac.build_maps(pages[1:])

    score = min([my_alamac.get_location(int(seed)) for seed in seed_nums])
    logger.info("****Answer:****")
    logger.info(score)
    return None
