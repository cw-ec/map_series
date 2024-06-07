from components import BulkMapToPDF

"""
This workflow performs a bulk export of maps from aprx files to pdf files. Similar to the aprx_to_pdf tool however this
version will iterate over several aprx projects instead of being limited to just one

    in_dir: This parameter should be the root directory that contains all of the .aprx files. All .aprx files in this 
            directory subfolders will be exported as well.                                                                                 
    out_dir: This parameter should link to the directory will take the exported maps. If maps of a matching name are 
             present in the file then they will be overwritten by the new maps.                                                               
    to_pdf_list: This parameter should contain a list of all aprx files to convert into pdf files. This option should be 
                 used when only needing to convert a subset of aprx files available in the input directory. Otherwise 
                 leave this parameter blank. 
    as_image: This parameter determines if the maps is exported as vector graphics or as an image. This is for specific 
              cases where the basemap does not render properly in the PDF. The default value of this is False.                               
    dpi: This parameter sets the dpi of the output PDF which effects its resolution. The default value for this parameter 
         is 300(dpi).                                                                                                                 


"""

BulkMapToPDF(
    in_dir=r"J:\DMT Map Series Analysis\Tests\TestData_Chris\New_343",
    out_dir=".\\data\\map_dump",
    #as_image=True,
    #dpi=96
)
