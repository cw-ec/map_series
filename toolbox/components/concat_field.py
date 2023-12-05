import sys, os
import pandas as pd
from toolbox.components import logging_setup


class ConcatField():
    """Takes a table and will concatonate the concat_field by using the id field"""

    def concatenator(self):
        "Performs the concatenation"

        self.logger.info("Loading in data")
        data = pd.read_excel(self.table, sheet_name=self.sheet_name)

        out_data = [] # empty list for out rows to go to
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
                    suffix = ''.join([d for d in suffix if not d.isdigit()])  # Drop all numbers from the suffix

                    to_concat.append(f"{prefix}{suffix}")

                if isinstance(c, int):
                    to_concat.append(str(c))

                else:
                    raise Exception(f"{type(c)} is an invalid type. Check data")

            # Create the concatenation or create a warning
            if len(to_concat) == 1:
                concated = f"{to_concat[0]}{self.separator}"
            elif len(to_concat) > 1:
                concated = f'{self.separator}'.join(to_concat)
            else:
                self.logger.warning(f"ID:{i} had no records to concatenate")

            out_row = i_data.iloc[0].copy()
            out_row[self.out_field] = concated

            out_data.append(out_row)
        out_df = pd.DataFrame(out_data)
        out_df[self.out_field] = out_df[self.out_field].astype(object)
        out_df.to_csv(os.path.join(self.out_directory, f"{self.in_tbl_nme}_concatenated.csv"),index=False)


    def __init__(self, table, id_field, concat_field, out_directory, separator=';', sheet_name=0):

        self.logger = logging_setup()

        self.table = table
        self.id_field = id_field
        self.concat_field = concat_field
        self.separator = separator
        self.out_directory = out_directory
        self.sheet_name = sheet_name

        self.in_tbl_nme = os.path.split(self.table)[-1].split('.')[0]
        self.out_field = f'{self.concat_field}_concat'
        self.concatenator()
        self.logger.info("DONE!")
