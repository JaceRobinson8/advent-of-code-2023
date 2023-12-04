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
    input_path = Path("./days/day_1/challenge_2/input/input.txt")
    cal_list = parse_input(input_path)
    sum_cal = sum([cal.cal_val for cal in cal_list])
    logger.info("****Final Answer****")
    logger.info(sum_cal)
