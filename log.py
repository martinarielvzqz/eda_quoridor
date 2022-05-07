import logging
import sys

from utils import Config

formatter = logging.Formatter(fmt="[%(asctime)s] %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# console
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(formatter)

# file
fh = logging.FileHandler(Config["log_path"])
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

logger.addHandler(sh)
logger.addHandler(fh)
