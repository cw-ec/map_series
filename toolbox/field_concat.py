from toolbox.components import ConcatField

"""

This tool concatenates a dataset and removes duplicates returning the concatenated field as a string with the values
separated by a common character. This tool will take a column of values clean non-essential characters and concatenate
all the values by the separator character. This will be returned in a single row and duplicated rows would be not be
retained.

For example:

        "002-0"
        "003-1"
        "005-0A"
        "005-1B"
        "010-9"

Would be concatenated to:
        
        "2;3;5A;5B;10"        

This workflow takes the following parameters:

    table: The path to the input excel file.
    
    id_field: The name of the field that the records will be concatenated against.
    
    concat_field: The name of the field to be concatenated.
    
    out_directory: The name of the directory that the concatenated file will be placed.
    
    separator: This optional parameter is the character that will be used to separate the concatenated field. The default
               value for this parameter is: ';'.

    sheet_name: This optional parameter is the name or index of the sheet to be concatenated. If using indexes note that
                they start at 0 so the first sheet in the excel file will be index 0. The default vale for this parameter
                is the first sheet in the excel document or 0.
"""

ConcatField(
    table="C:\\map_series\\data\\EMV_Report_2021-09-20.xlsx",
    id_field='SITE_ID',
    concat_field='PD / SV',
    out_directory="C:\\map_series\\data",
    separator=';',
    sheet_name=0
)
