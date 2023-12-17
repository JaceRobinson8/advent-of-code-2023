from pathlib import Path
from common.utils import parse_input
import logging
from rich.logging import RichHandler
from functools import reduce

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Configure logging with RichHandler
    logging.basicConfig(
        level=logging.DEBUG, format="%(message)s", handlers=[RichHandler()]
    )
    input_path = Path("./days/day_6/challenge_1/input/input.txt")
    races = parse_input(input_path)
    # product all records
    res = int(reduce(lambda x, y: x * y, [r.beat_record_count for r in races], 1.0))
    logger.info(f"****Answer: {res}****")
