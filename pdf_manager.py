from components import MapPdfSort

"""
This script contains all scripts related to the sorting and consolidation of pdfs in the map series workflow. 

Parameters:

    dump_dir: This is the path to the folder containing all the pdf files exported from map series. All pdfs in this 
            folder must meet the required naming convention in order to be properly processed by this script.

    sorted_dir: This should be the path to the destination folder for the pdfs. It can either be empty or contain 
                outputs from a previous run of this script.   

"""

MapPdfSort(
    dump_dir=r'C:\map_series\data\MS_ExportedMaps\Dump_AllMaps',
    sorted_dir=r'C:\map_series\data\MS_ExportedMaps\sorted'
)
