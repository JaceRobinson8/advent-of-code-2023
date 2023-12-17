from pathlib import Path
from common.utils import parse_input, key
import logging
from rich.logging import RichHandler

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Configure logging with RichHandler
    logging.basicConfig(
        level=logging.DEBUG, format="%(message)s", handlers=[RichHandler()]
    )
    input_path = Path("./days/day_7/challenge_2/input/input.txt")
    game = parse_input(input_path)
    logger.debug("before")
    logger.debug(game.rounds)
    game.rounds.sort(key=key)
    logger.debug("after")
    logger.debug(game.rounds)
    res = sum([(idx + 1) * r.bid for idx, r in enumerate(game.rounds)])
    logger.info(f"***Answer: {res}****")
