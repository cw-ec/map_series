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

def create_verify_gdf(gdb_path):
    """Checks to see if input pdb path exists and if not create it"""
    from arcpy import CreateFileGDB_management

    if not os.path.exists(gdb_path):
        root = os.path.split(gdb_path)[0]
        gdb_name = os.path.split(gdb_path)[-1]

        # If root doesn't exist create it
        if not os.path.exists(root):
                os.makedirs(root)

        CreateFileGDB_management(root, gdb_name)

