from pathlib import Path
from common.utils import parse_input
import logging
from rich.logging import RichHandler

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Configure logging with RichHandler
    logging.basicConfig(
        level=logging.DEBUG, format="%(message)s", handlers=[RichHandler()]
    )
    N_RED_MAX = 12
    N_GREEN_MAX = 13
    N_BLUE_MAX = 14
    input_path = Path("./days/day_2/challenge_1/input/input.txt")
    games = parse_input(input_path)
    result = sum(
        [g.id for g in games if g.check_possible(N_RED_MAX, N_GREEN_MAX, N_BLUE_MAX)]
    )
    logger.info("****Answer:****")
    logger.info(result)
