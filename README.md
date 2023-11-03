# map_series

This repository exist for development and testing various components of the map series proof of concept(PoC).
More documentation to be added as development progresses.

### Requirements

This project will require the installation of ArcGIS Pro as access to the default ArcGIS Pro python environment is 
required to run these scripts. Ensure that you have a valid licence before running the scripts.

## Component 1: Map PDF sorting and consolidation

This component sorts all pdf maps from a given folder into the approved folder structure. 

## Component 2: Export Maps as PDF files

This component contain scripts designed to produce and manipulate pdf files of the maps produced by map series.

### pdf_management.py

This script is designed to sort output pdf maps into the approved folder structure for this project. Consolidates the 
pdfs into a master doc where specified.

## Component 3: Data Downloads and Updates

This component consists of script designed to download data and make it usable for ArcGIS Pro and Map Series. Scripts 
in this component may injest internal or external datasets clean and prep them to a format best suited for the map 
series project.

### update_placenames.py

This script downloads a new version of the NRCAN placenames data and replaces existing copies of this data in the
central map series GDB. The current version of this file in this repo is unfinished.
