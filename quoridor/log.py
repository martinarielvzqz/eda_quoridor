import logging
import os
import sys

from quoridor.constants import (
    LOG_DIR,
    LOG_FILE,
    LOG_GAMES_DIR
)


os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(LOG_GAMES_DIR, exist_ok=True)


def get_logger(log_file: str = LOG_FILE, level: int = logging.DEBUG):
    logger = logging.getLogger(log_file)
    logger.setLevel(level)
    formatter = logging.Formatter(fmt="[%(asctime)s] %(levelname)s - %(message)s")

    # console
    sh = logging.StreamHandler(sys.stdout)
    logger.setLevel(level)
    sh.setFormatter(formatter)

    # file
    fh = logging.FileHandler(log_file)
    logger.setLevel(level)
    fh.setFormatter(formatter)

    logger.addHandler(sh)
    logger.addHandler(fh)
    return logger


logger = get_logger()
