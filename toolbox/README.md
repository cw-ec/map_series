# Component Tools Documentation

This folder contains the files needed to run each workflow. Detailed descriptions of each tool and its parameters are given
in this document which is reflected in .py files found in this folder.

## Component 1: PDF Map Production and Post Processing

Below is detailed documentation of each tool in component 1 dealing with the creation organization and manipulation of
map pdfs.

### APRX to PDF

This workflow takes a .aprx file containing a map series and exports the maps as individual pdf files following the 
approved naming convention: "FEDCount_PollType_MapType". If not following this naming convention the .aprx file will not
be processed. The script outputs pdf files with the following naming convention: "PollType_FedNum_InsetType/PageNum".
The main script for this workflow is called 'aprx_to_pdf.py' and it takes the following parameters:

| Name      |  Type   | Required | Description                                                                                                                                                                                                |
|-----------|:-------:|:--------:|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| aprx_path | String  | Required | This parameter is the path to the .aprx file that contains the maps to be exported.                                                                                                                        |
| out_dir   | String  | Required | This parameter should link to the directory will take the exported maps. If maps of a matching name are present in the file then they will be overwritten by the new maps.                                 |
| as_image  | Boolean | Optional | This parameter determines if the maps is exported as vector graphics or as an image. This is for specific cases where the basemap does not render properly in the PDF. The default value of this is False. |
| dpi       | Integer | Optional | This parameter sets the dpi of the output PDF which effects its resolution. The default value for this parameter is 300.                                                                                   |

### Bulk APRX to PDF

This workflow utilizes the same code as the APRX to PDF script however this workflow add the functionality to bulk
export the maps from the aprxs contained in a given directory and its subdirectories. The main script for this workflow 
is called 'bulk_aprx_to_pdf.py' and it takes the following parameters:

| Name        |  Type   | Required | Description                                                                                                                                                                                                                              |
|-------------|:-------:|:--------:|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| in_dir      | String  | Required | This parameter should be the root directory that contains all of the .aprx files. All .aprx files in this directory subfolders will be exported as well.                                                                                 |
| out_dir     | String  | Required | This parameter should link to the directory will take the exported maps. If maps of a matching name are present in the file then they will be overwritten by the new maps.                                                               |
| to_pdf_list |  List   | Optional | This parameter should contain a list of all aprx files to convert into pdf files. This option should be used when only needing to convert a subset of aprx files available in the input directory. Otherwise leave this parameter blank. |
| as_image    | Boolean | Optional | This parameter determines if the maps is exported as vector graphics or as an image. This is for specific cases where the basemap does not render properly in the PDF. The default value of this is False.                               |
| dpi         | Integer | Optional | This parameter sets the dpi of the output PDF which effects its resolution. The default value for this parameter is 300.                                                                                                                 |

### PDF Management

This workflow sorts and creates consolidated versions of the exported pdf maps produced by map series. This workflow can 
be accessed via the pdf_manager.py script which takes the following parameters:

| Name       | Type   | Required | Description                                                                                                                                                                                              |
|------------|--------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| dump_dir   | string | Required | This is the path to the folder containing all the pdf files exported from map series. All pdfs in this folder must meet the required naming convention in order to be properly processed by this script. |
| sorted_dir | string | Required | This should be the path to the destination folder for the pdfs. It can either be empty or contain outputs from a previous run of this script.                                                            |

### PDF Consolidation

This workflow consolidates pdf files based on the approved map series folder structure and exports them into a zipfile
at the root of the directory that shares its FED Number.

This workflow takes the following parameters:

| Name          | Type           | Required | Description                                                                                                                                                     |
|---------------|----------------|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| in_dir        | string         | Required | Path to the directory that contains all pdfs to be consolidated. Must be organized into the approved file structure for the map series project.                 |
| feds_to_combo | array(integer) | Optional | This optional parameter should be and array of FED numbers as integers. Only pdfs in folders with this name will be consolidated when this parameter is filled. |


## Component 2: Data Downloads and Updates

Below is detailed documentation of each tool in component 2 dealing with the ingestion an updating of data needed to 
create the maps in maps series. At this time this section only contains example scripts.

### Update PlaceNames

This script downloads and preprocesses the NRCan place names dataset for use in map creation. Not in full working order but 
a skeleton for future development has been implemented in this repository as an example. 

| Name         | Type   | Required | Description                                                                                                     |
|--------------|--------|----------|-----------------------------------------------------------------------------------------------------------------|
| geo_name_url | string | Required | This parameter is the url to the online zipfile that is to be downloaded and processed.                         |
| output_gdb   | string | Required | The gdb  in which the output feature classes will be placed. Should be preexisting.                             |
| fed_num_fc   | String | Required | The full path to the feature class or shapefile that contains the FED data to be joined to the downloaded data. |
