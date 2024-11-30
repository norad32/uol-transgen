import logging
import argparse
from transition_generator.transition_generator import TransitionGenerator

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Generate UO Landscaper Transition XML."
    )
    parser.add_argument(
        "-i",
        "--input-transitions",
        type=str,
        required=True,
        help="Specify the input Transition XML file to use",
    )
    parser.add_argument(
        "-a",
        "--terrain-a",
        type=str,
        required=True,
        help="Specify Terrain A name or ID.",
    )
    parser.add_argument(
        "-b",
        "--terrain-b",
        type=str,
        required=False,
        help="Specify Terrain B name or ID. If not used Transitions for all Terrains are generated.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = main()
    try:
        generator = TransitionGenerator(args)
        generator.run()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        exit(1)
