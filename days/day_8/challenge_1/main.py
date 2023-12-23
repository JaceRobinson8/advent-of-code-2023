from pathlib import Path
from common.utils import parse_input, Node
import logging
from rich.logging import RichHandler
from itertools import cycle

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Configure logging with RichHandler
    logging.basicConfig(
        level=logging.DEBUG, format="%(message)s", handlers=[RichHandler()]
    )
    DESTINATION = Node("ZZZ")
    input_path = Path("./days/day_8/challenge_1/input/input.txt")
    insts, my_map = parse_input(input_path)
    for steps, inst in enumerate(cycle(insts)):
        my_map.go_next_location(inst)
        if my_map.current_loc == DESTINATION:
            break
    logger.info(f"****Answer: {steps+1}****")
