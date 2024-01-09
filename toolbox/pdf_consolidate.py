from components import PDFConsolidator

"""
This workflow consolidates pdf files based on the approved map series folder structure and exports them into a zipfile
at the root of the directory that shares its FED Number.

This workflow takes the following parameters:

    in_dir: Path to the directory that contains all pdfs to be consolidated. Must be organized into the approved file 
            structure for the map series project. 
    feds_to_combo: This optional parameter should be and array of FED numbers as integers. Only pdfs in folders with 
                   this name will be consolidated when this parameter is filled.


"""

PDFConsolidator(
    in_dir="..\\data\\sorted",
    #feds_to_combo=[24002, 24013]
)
