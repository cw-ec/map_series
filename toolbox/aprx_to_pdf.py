from components import MapToPDF

"""
This script is an experimental script used to compare the export times between the built in tools in arcgis pro and
similar tools available in ArcGIS Pro

    aprx_path: This parameter is the path to the .aprx file that contains the maps to be exported.
    
    out_dir: This Parameter should link to the directory will take the exported maps. If maps of a matching name are 
             present in the file then they will be overwritten by the new maps.
    
    as_image: This optional parameter determines if the map is exported as vector graphics or as an image. This is 
              for specific cases where the basemap does not render properly in the PDF. The default value of this is 
              False.
    
    dpi: This optional parameter sets the dpi of the output PDF which effects its resolution. The default value for 
         this parameter is 300.
    
    page_number_field_name: This optional parameter sets the field used as the page number in the map series. It also 
                            uses the values in this field to set the name for each pdf documents. The default value for 
                            this parameter is "PageCode".   
"""

MapToPDF(
    aprx_path=r"J:\DMT Map Series Analysis\Tests\TestData_Chris\New_343\MS343_OV_PEI_RuraMed\MS343_OV_PEI_RuralMed.aprx",
    out_dir="..\\data\\pdf",
    as_image=True,
    dpi=150
)
