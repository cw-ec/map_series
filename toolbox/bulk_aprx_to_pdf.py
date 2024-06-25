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
                 this parameter should not be included in the tool call or should be commented out. 
    
    as_image: This parameter determines if the maps is exported as vector graphics or as an image. This is for specific 
              cases where the basemap does not render properly in the PDF. The default value of this is True.                               
    
    dpi: This parameter sets the dpi of the output PDF which effects its resolution. The default value for this parameter 
         is 150 (dpi). 
         
    page_number_field_name: This optional parameter sets the field used as the page number in the map series. It also 
                            uses the values in this field to set the name for each pdf documents. The default value for 
                            this parameter is "PageCode".                                                                                                                


"""

BulkMapToPDF(
    in_dir="..\\data\\raw",
    out_dir="..\\data\\pdf",
    # to_pdf_list = [],
    as_image=True,
    dpi=150,
    page_number_field_name='PageCode'
)
