from components import PDFConsolidator

"""
This workflow consolidates pdf files based on the approved map series folder structure and exports them into a zipfile
at the root of the directory that shares its FED Number.

This workflow takes the following parameters:



"""

PDFConsolidator(
    in_dir=".\\data\\sorted",
    feds_to_combo=[24002, 24013]
)
