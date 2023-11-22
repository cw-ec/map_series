from components import UpdatePlaceNames

"""

This script controls the update data scripts

This script takes 3 inputs parameters:

    - geo_name_url: This parameter is the url to the online zipfile that is to be downloaded and processed.
    - output_gdb: The gdb  in which the output feature classes will be placed. Should be preexisting.
    - fed_num_fc: The full path to the feature class or shapefile that contains the FED data to be joined to the downloaded
    data.  


"""

UpdatePlaceNames(
        geo_name_url="https://ftp.cartes.canada.ca/pub/nrcan_rncan/vector/geobase_cgn_toponyme/prov_shp_eng/cgn_canada_shp_eng.zip",
        output_gdb=".\\data\\MapSeriesGDB.gdb",
        fed_num_fc=".\\data\\MapSeriesGDB.gdb\\EGD_REDIS_2023_FED_A_FINAL_CRT_Copied08Sept2023",
    )
