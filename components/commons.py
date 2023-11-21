import logging
import sys
import os
from datetime import datetime


def logging_setup(log_dir=".\\"):
    """Sets up logging takes one parameter to set a directory for the output log file"""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(log_dir, f"{datetime.today().strftime('%d-%m-%Y')}_log.log")),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger()


def create_dir(path:str) -> None:
    """Check if directory exists and if it doesn't create it."""
    if not os.path.exists(path):
        os.makedirs(path)
