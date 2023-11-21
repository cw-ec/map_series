from components import MapToPDF

"""
This script is an experimental script used to compare the export times between the built in tools in arcgis pro and
similar tools available in ArcGIS Pro

    aprx_path: This parameter is the path to the .aprx file that contains the maps to be exported.
    
    out_dir: This Parameter should link to the directory will take the exported maps. If maps of a matching name are 
             present in the file then they will be overwritten by the new maps.
    
    as_image: This optional parameter determines if the maps is exported as vector graphics or as an image. This is 
              for specific cases where the basemap does not render properly in the PDF. The default value of this is 
              False.
    dpi: This optional parameter sets the dpi of the output PDF which effects its resolution. The default value for 
         this parameter is 300.   
"""

MapToPDF(
    aprx_path=r"J:\DMT Map Series Analysis\Tests\TestData_Chris\MS338_P_LrgInset_Ont\MS338_P_LrgInset_Ont.aprx",
    out_dir=r"J:\DMT Map Series Analysis\Tests\TestData_Chris\test_output",\
    as_image=True,
    dpi=300
)
