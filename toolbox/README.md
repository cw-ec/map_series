# Component Tools Documentation

This folder contains the files needed to run each workflow. Detailed descriptions of each tool and its parameters are given
in this document which is reflected in .py files found in this folder.

## Common Outputs

All tools will produce a log file which will contain all messages and errors from the run of the tool. This allows for 
a user to validate that tool finished processing or identify and error that occurred without needing the original window.

The contents of the log file will look like this:

    2023-11-22 11:23:13,832 [INFO] Export process started
    2023-11-22 11:23:25,432 [INFO] Exporting:P_35083_B01
    2023-11-22 11:23:51,729 [INFO] Page Exported
    2023-11-22 11:23:51,735 [INFO] Exporting:P_35083_B02
    2023-11-22 11:24:05,163 [INFO] Page Exported
    2023-11-22 11:24:05,170 [INFO] Exporting:P_35083_B03
    2023-11-22 11:24:18,131 [INFO] Page Exported
    2023-11-22 11:24:18,139 [INFO] Exporting:P_35083_B04
    2023-11-22 11:24:31,258 [INFO] Page Exported
    2023-11-22 11:24:31,259 [INFO] DONE!

Note that the above log contains a timestamp, the type of information the message is intended to convey and the message itself.
There are several types of message that can be conveyed in this file.

- INFO: Standard Message meant to convey some generic status of the tool
- WARNING: Something has occurred while running the tool that raised a warning. While the tool will still continue to run
            after a warning it would be noted as whatever caused the warning may affect the  quality output.
- ERROR: An error has occurred that has caused the tool to fail. No outputs are produced when an error occurs. 

The majority of all messages will be INFO used to indicate the tools progress in its process. Any WARNING or ERROR messages
should be considered abnormal as they indicate a problem and should be investigated.

## Component 1: PDF Map Production and Post Processing

The section below contains detailed documentation for each tool in component 1 dealing with the creation, organization, 
and manipulation of map pdfs.

### APRX to PDF (aprx_to_pdf.py)

This workflow takes a .aprx file containing a map series and exports the maps as individual pdf files following the 
approved naming convention: "FEDCount_PollType_MapType". If not following this naming convention the .aprx file will not
be processed. The script outputs pdf files with the following naming convention: "PollType_FedNum_InsetType/PageNum".
The main script for this workflow is called 'aprx_to_pdf.py' and it takes the following parameters:

| Name      |  Type   | Required | Description                                                                                                                                                                                                |
|-----------|:-------:|:--------:|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| aprx_path | String  | Required | This parameter is the path to the .aprx file that contains the maps to be exported.                                                                                                                        |
| out_dir   | String  | Required | This parameter should link to the directory will take the exported maps. If maps of a matching name are present in the file then they will be overwritten by the new maps.                                 |
| as_image  | Boolean | Optional | This parameter determines if the maps is exported as vector graphics or as an image. This is for specific cases where the basemap does not render properly in the PDF. The default value of this is False. |
| dpi       | Integer | Optional | This parameter sets the dpi of the output PDF which effects its resolution. The default value for this parameter is 150.                                                                                   |

### Bulk APRX to PDF (bulk_aprx_to_pdf.py)

This workflow utilizes the same code as the APRX to PDF script however this workflow add the functionality to bulk
export the maps from the aprxs contained in a given directory and its subdirectories. The main script for this workflow 
is called 'bulk_aprx_to_pdf.py' and it takes the following parameters:

| Name        |  Type   | Required | Description                                                                                                                                                                                                                              |
|-------------|:-------:|:--------:|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| in_dir      | String  | Required | This parameter should be the root directory that contains all of the .aprx files. All .aprx files in this directory subfolders will be exported as well.                                                                                 |
| out_dir     | String  | Required | This parameter should link to the directory will take the exported maps. If maps of a matching name are present in the file then they will be overwritten by the new maps.                                                               |
| to_pdf_list |  List   | Optional | This parameter should contain a list of all aprx files to convert into pdf files. This option should be used when only needing to convert a subset of aprx files available in the input directory. Otherwise leave this parameter blank. |
| as_image    | Boolean | Optional | This parameter determines if the maps is exported as vector graphics or as an image. This is for specific cases where the basemap does not render properly in the PDF. The default value of this is False.                               |
| dpi         | Integer | Optional | This parameter sets the dpi of the output PDF which effects its resolution. The default value for this parameter is 150.                                                                                                                 |

### PDF Management (pdf_manager.py)

This workflow sorts and creates consolidated versions of the exported pdf maps produced by map series. This workflow can 
be accessed via the pdf_manager.py script which takes the following parameters:

| Name       |   Type   |  Required  | Description                                                                                                                                                                                              |
|------------|:--------:|:----------:|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| dump_dir   |  string  |  Required  | This is the path to the folder containing all the pdf files exported from map series. All pdfs in this folder must meet the required naming convention in order to be properly processed by this script. |
| sorted_dir |  string  |  Required  | This should be the path to the destination folder for the pdfs. It can either be empty or contain outputs from a previous run of this script.                                                            |

### PDF Consolidation (pdf_consolidation.py)

This workflow consolidates pdf files based on the approved map series folder structure and exports them into a zipfile
at the root of the directory that shares its FED Number.

This workflow takes the following parameters:

| Name          |       Type       |  Required  | Description                                                                                                                                                     |
|---------------|:----------------:|:----------:|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| in_dir        |      string      |  Required  | Path to the directory that contains all pdfs to be consolidated. Must be organized into the approved file structure for the map series project.                 |
| feds_to_combo |  array(integer)  |  Optional  | This optional parameter should be and array of FED numbers as integers. Only pdfs in folders with this name will be consolidated when this parameter is filled. |


## Component 2: Data Updates and Manipulation

Below is detailed documentation of each tool in component 2 dealing with the ingestion an updating of data needed to 
create the maps in maps series. This includes tools that create custom fields, and custom subsets so that the data can
be better utilized during the map creation phase.

### Update PlaceNames (update_placenames.py)

This script downloads and preprocesses the NRCan place names dataset for use in map creation. This script downloads the 
data from the source and adds it as subsets to a given geodatabase. These subsets are predefined and are used as part of 
the mapping process. To add a subset the source code of the script will need to be altered. There is an options to download
the data again if it has been updated. When downloaded the subsets will be created from that downloaded shapefile. If the 
option to download the data is not selected please ensure that the placenames file is placed in a folder called 'data' at the
root of this repository or the tool will not function as expected. Ensure that the shapefile retains its original name
"cgn_canada_shp_eng.shp" and that all fields retain their original names.

| Name              |  Type   | Required | Description                                                                                                                                                                                            |
|-------------------|:-------:|:--------:|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| geo_name_url      | string  | Required | This parameter is the url to the online zipfile that is to be downloaded and processed.                                                                                                                |
| output_gdb        | string  | Required | The gdb  in which the output feature classes will be placed. Should be preexisting.                                                                                                                    |
| fed_num_fc        | String  | Required | The full path to the feature class or shapefile that contains the FED data to be joined to the downloaded data.                                                                                        |
| download_new_data | Boolean | Optional | Download a new version of th NR placenames data from the source. The default value is False.                                                                                                           |
| pn_shp_nme        | String  | Optional | Name of the shapefile to be subset. Default value is name downloaded from source do not change this parameter if downloading a new version of the data. The default value is "cgn_canada_shp_eng.shp". |

### Concatenate Field (field_concat.py)

This tool concatenates a dataset and removes duplicates returning the concatenated field as a string with the values
separated by a common character. This tool will take a column of values cleans non-essential characters and concatenates
all the values using the separator character. This will be returned in a single row and duplicated rows would be not be
retained.

For example:

        "002-0"
        "403-1"
        "005-0A"
        "005-1B"
        "010-9"

Would be concatenated to:
        
        "2;403-1;5A;5-1B;10-9"  

| Name          |       Type        | Required | Description                                                                                                                                                                                                                                                       |
|---------------|:-----------------:|:--------:|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| table         |      string       | Required | The path to the input excel file.                                                                                                                                                                                                                                 |
| id_field      |      string       | Required | The name of the field that the records will be concatenated against.                                                                                                                                                                                              |
| concat_field  |      string       | Required | The name of the field to be concatenated.                                                                                                                                                                                                                         |
| out_directory |      string       | Required | The name of the directory that the concatenated file will be placed.                                                                                                                                                                                              |
| separator     |      string       | Optional | This optional parameter is the character that will be used to separate the concatenated field. The default value for this parameter is: ';'.                                                                                                                      |
| sheet_name    | integer or string | Optional | This optional parameter is the name or index of the sheet to be concatenated. If using indexes note that they start at 0 so the first sheet in the excel file will be index 0. The default vale for this parameter is the first sheet in the excel document or 0. |

### Dissolver

This tool takes an input dataset and creates a dissolved version based on the input dissolve fields. Each dissolved version is placed in the output geodatabase.

| Name        |     Type      | Required | Description                                                                                                                                                                                                                                                        |
|-------------|:-------------:|:--------:|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| in_data     |    string     | Required | The path to the dataset that contains the features to be dissolved.                                                                                                                                                                                                |
| out_gdb     |    string     | Required | The path to the geodatabase where the features will be created. If the geodatabase doesn't exist it will be created.                                                                                                                                               |
| diss_fields | tuple or list | Optional | A list or tuple of field names (as string) that will be used to guide the dissolution tool. If an empty list is passed into this parameter then all geometry in the input dataset will be dissolved the default of this parameter is: ["ADV_UID", "SITE_AREA_UID"] |

