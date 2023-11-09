import logging
import sys
import os
from datetime import datetime


def logging_setup(log_dir=os.path.curdir) -> logging.getLogger():
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
