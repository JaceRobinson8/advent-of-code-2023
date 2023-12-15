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
    input_path = Path("./days/day_4/challenge_2/input/input.txt")
    card_stack = parse_input(input_path)
    score = card_stack.start()
    logger.info("****Answer:****")
    logger.info(score)
