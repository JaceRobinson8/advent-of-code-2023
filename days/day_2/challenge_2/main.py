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
    input_path = Path("./days/day_2/challenge_2/input/input.txt")
    games = parse_input(input_path)
    result = sum([g.get_power() for g in games])
    logger.info("****Answer:****")
    logger.info(result)
