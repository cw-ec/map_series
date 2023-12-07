import sys, os
import csv
import pandas as pd
from toolbox.components import logging_setup, create_dir, to_dataframe


class ConcatField:
    """Takes a table and will concatonate the concat_field by using the id field"""

    def concatenator(self) -> None:
        "Performs the concatenation"

        self.logger.info("Loading in data")
        data = to_dataframe(self.table, sheet=self.sheet_name)

        out_data = []  # empty list for out rows to go to
        # Iterate over all the unique values in the id_field
        self.logger.info("Creating concatenations")
        for i in data[self.id_field].unique():
            i_data = data[data[self.id_field] == i].copy()
            to_concat = []
            # Iterate over the items in concat field to clean concat and append to list
            for c in i_data[self.concat_field].tolist():

                if isinstance(c, str):
                    # Strip away non-essential numbers
                    prefix = c.split('-')[0]
                    suffix = c.split('-')[1]

                    prefix = prefix.lstrip('0')  # Strip all 0's from the start of the prefix
                    suffix = ''.join([d for d in suffix if not (d.isdigit()) or (d != "0")])  # Drop all numbers from the suffix

                    to_concat.append(f"{prefix}{suffix}")
                elif isinstance(c, int):
                    to_concat.append(str(c))
                else:
                    raise Exception(f"{type(c)} is an invalid type. Check data")

            # Create the concatenation or create a warning
            if len(to_concat) == 1:
                concated = str(to_concat[0])
            elif len(to_concat) > 1:
                concated = f'{self.separator}'.join(to_concat)
            else:
                self.logger.warning(f"ID:{i} had no records to concatenate")

            out_row = i_data.iloc[0].copy()
            out_row[self.out_field] = concated
            out_data.append(out_row)

        # Convert data to a dataframe qc and export
        out_df = pd.DataFrame(out_data)
        out_df[self.out_field] = out_df[self.out_field].astype(object)
        out_df.drop(labels=self.concat_field, axis=1, inplace=True)  # Drop the concat_field as it is no longer needed
        self.logger.info(f"Exporting: {self.in_tbl_nme}_concatenated.csv")
        out_df.to_csv(os.path.join(self.out_directory, f"{self.in_tbl_nme}_concatenated.csv"),
                      index=False,
                      )

    def is_valid(self, table, id_field, concat_field, out_directory, separator=';', sheet_name=0):
        """Validates the inputs"""

        self.logger.info("Validating inputs")
        if not isinstance(table, str):
            raise Exception("Parameter: 'table' must be a string")
        if not isinstance(id_field, str):
            raise Exception("Parameter: 'id_field' must be a string")
        if not isinstance(concat_field, str):
            raise Exception("Parameter: 'concat_field' must be a string")
        if not isinstance(out_directory, str):
            raise Exception("Parameter: 'out_directory' must be a string")
        if not isinstance(separator, str):
            raise Exception("Parameter: 'separator' must be a string")
        if not isinstance(sheet_name, str) and not isinstance(sheet_name, int):
            raise Exception(f"Parameter: 'sheet_name' must be a string or an integer")

    def __init__(self, table, id_field, concat_field, out_directory, separator=';', sheet_name=0):

        # Logging setup and validation
        self.logger = logging_setup()
        self.is_valid(table, id_field, concat_field, out_directory, separator, sheet_name)

        # If all inputs are valid assign
        self.table = table
        self.id_field = id_field
        self.concat_field = concat_field
        self.separator = separator
        self.out_directory = out_directory
        self.sheet_name = sheet_name

        # Some derived inputs
        self.in_tbl_nme = os.path.split(self.table)[-1].split('.')[0]
        self.out_field = f'{self.concat_field}_concat'

        # Run the process
        create_dir(self.out_directory)
        self.concatenator()
        self.logger.info("DONE!")
