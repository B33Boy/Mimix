import logging
import sys


def configure_logging(level = logging.INFO):
    logging.basicConfig(
        level = level,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.getLogger("discord").setLevel(logging.INFO)