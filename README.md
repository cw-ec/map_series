# Map Series

 The purpose of this repository is for development and testing various components of the map series proof of concept (PoC).
More documentation to be added as development progresses.

### Requirements

This project will require the installation of ArcGIS Pro as access to the default ArcGIS Pro python environment as well
as arcpy are required to run the projects workflows. Ensure that you have a valid licence associated with your installation
of Arcgis Pro before running the scripts.

### Usage

Each of the workflows within this project follows a standardized structure and the instructions on how to use each 
workflow will be relatively similar. Any differences in instructions will be noted in the documentation for that specific
workflow.

To operate a tool follow these instructions:
    
1. Select the appropriate .py file from the main folder of this repository and open it in an IDE. At Elections Canada Visual 
Studio Code is available for this purpose (Notepad++ is an alternative text editor).
2. Alter the parameters to reflect your desired inputs referring to the descriptions within the .py file or in the workflows 
documentation as needed.
3. If running the file from an IDE (pycharm, VScode, etc.) run the file as normal. If an IDE is not available to you see 
the directions for running the file from the command line below.

   - Open the search window from the bottom left of your screen and search for 'Python Command Prompt'

     ![Python Command Prompt Search](./docs/imgs/PCP_img.png)
   - Ensure that the python environment is the default arcgis pro python env. This is usually named something like 
   'arcgispro-py3' and should be seen in the brackets in the far left of the command prompt window as seen below.
   
     <img alt="Python Command Prompt correctly formatted" height="150" src="./docs/imgs/PCP_base.png" width="800"/>
   - Using the 'cd' command navigate to the toolbox subdirectory of this repository
   
     <img alt="Python Command Prompt correctly formatted" height="100" src="./docs/imgs/PCP_correct_dir.png" width="800"/>
   - Run the workflow if your choice using the following command format: python 'name of python file'.py This should
   trigger your desired workflow to start running. If an error is returned instead verify the prior steps and try again.

     <img alt="Python Command Prompt Search" height="150" src="./docs/imgs/PCP_run_workflow.png" width="800"/>

## Toolbox

All tools developed as part of this project can be found in the toolbox subdirectory if this repository. Detailed
documentation of each tool can be found in that folder. The tools in the toolbox are organized into several different
components each containing tools with a different general purpose. A brief description of each component can be found below.

### Component 1: PDF Map Production and Post Processing

This component contain scripts designed to produce and manipulate pdf files of the maps created by map series.

### Component 2: Data Downloads and Updates

This component consists of script designed to download data and make it usable for ArcGIS Pro and Map Series. Scripts 
in this component may ingest internal or external datasets clean and prep them to a format best suited for the map 
series project.
