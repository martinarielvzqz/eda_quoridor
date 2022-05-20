import logging
import sys

from quoridor.constants import LOG_FILE


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
