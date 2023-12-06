import logging
import sys
import os
import pandas as pd
from datetime import datetime


def logging_setup(log_dir=".\\") -> logging.getLogger():
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


def create_dir(path: str) -> None:
    """Check if directory exists and if it doesn't create it."""
    if not os.path.exists(path):
        os.makedirs(path)

def create_verify_gdf(gdb_path: str) -> None:
    """Checks to see if input pdb path exists and if not create it"""
    from arcpy import CreateFileGDB_management

    if not os.path.exists(gdb_path):
        root = os.path.split(gdb_path)[0]
        gdb_name = os.path.split(gdb_path)[-1]

        # If root doesn't exist create it
        if not os.path.exists(root):
            os.makedirs(root)

        CreateFileGDB_management(root, gdb_name)


def to_dataframe(to_import: str, sheet=0) -> pd.DataFrame:
    """Import the given path into a pandas dataframe. Returns that pandas dataframe

    to_import = the path to the data to import into the dataframe. Required

    sheet = Name of the sheet to import into a dataframe. Can be integer or text of name (str)

    """

    path_list = os.path.split(to_import)
    f_type = path_list[0].split('.')[-1]

    if f_type == 'csv':
        return pd.read_csv(to_import)
    elif f_type in ["xlsx", "xls"]:
        return pd.read_excel(to_import, sheet_name=sheet)
    else:
        raise Exception(f"File Extension: {f_type} not yet handled by this function")
