# Map Series

 The purpose of this repository is for development and testing various components of the map series proof of concept (PoC).
More documentation to be added as development progresses.

### Requirements

This project will require the installation of ArcGIS Pro as access to the default ArcGIS Pro python environment is 
required to run these scripts. Ensure that you have a valid licence before running the scripts.

### Usage

The components follow a standardized workflow and the instructions on how to use each tool will be relatively similar.
To operate a tool follow these instructions:
    
1. Select the appropriate .py file from the main folder of this repository and open it in the IDE of your choice 
(Notepad++ is a good alternative if no traditional IDE is available).
2. Alter the parameters if the inputs referring to the infile descriptions of the parameters as needed
3. If running the file from a traditional IDE run the file as normal. If one is not available to you see the directions
below.

   - Open the search window from the bottom right of your screen and search for 'Python Command Prompt'
   - Ensure that the python environment 
   - Using the 'cd' command navigate to the main folder of this repository
   - Run the workflow if your choice using the following command format: python 'name of python file'.py

## Component 1: Export Maps as PDF files

This component contain scripts designed to produce and manipulate pdf files of the maps produced by map series.

### PDF Management

This workflow sorts and creates consolidated versions of the exported pdf maps produced by map series. This workflow can 
be accessed via the pdf_manager.py script which takes the following parameters:

| Name       | Type   | Description                                                                                                                                                                                              |
|------------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| dump_dir   | string | This is the path to the folder containing all the pdf files exported from map series. All pdfs in this folder must meet the required naming convention in order to be properly processed by this script. |
| sorted_dir | string | This should be the path to the destination folder for the pdfs. It can either be empty or contain outputs from a previous run of this script.                                                            |

## Component 2: Data Downloads and Updates

This component consists of script designed to download data and make it usable for ArcGIS Pro and Map Series. Scripts 
in this component may ingest internal or external datasets clean and prep them to a format best suited for the map 
series project.

### Update PlaceNames

This script downloads and preprocesses the NRCan place names dataset for use in map creation.
