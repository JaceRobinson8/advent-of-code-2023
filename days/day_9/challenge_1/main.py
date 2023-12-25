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
    input_path = Path("./days/day_9/challenge_1/input/test.txt")
    stacks = parse_input(input_path)
    res = sum([s.top_extrap_val for s in stacks])
    logger.info(f"****Answer: {res}****")
