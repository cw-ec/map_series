import requests
import zipfile
import os
import io
import logging
import arcpy
import pandas as pd
import arcgis
from arcgis.features import GeoAccessor, GeoSeriesAccessor
from arcgis.geometry import SpatialReference

"""
The purpose of this script is to download the geoplacenames file and then save the subtypes (under the generic field) as 
separate featureclasses in a given geodatabase
"""

# Temp Spot for Inputs
spatial_ref = str(4269)
geo_name_url = "https://ftp.cartes.canada.ca/pub/nrcan_rncan/vector/geobase_cgn_toponyme/prov_shp_eng/cgn_canada_shp_eng.zip"
temp_dir = r"C:\map_series_tests\data"
output_gdb = r"C:\map_series_tests\data\MapSeriesGDB.gdb"
file_name = "cgn_canada_shp_eng.shp"
fed_num_fc = r"C:\map_series_tests\data\MapSeriesGDB.gdb\EGD_REDIS_2023_FED_A_FINAL_CRT_Copied08Sept2023"
filter_field = 'GENERIC'
subtypes = {
    'Airport': ['Airport', 'Airfield'],
    'CFB': ['Canadian Forces Base', 'Canadian Forces Camp', 'Canadian Forces Range and/or Training Area (C.F.T.A.)',
            'Canadian Forces Station'],
}

# Sets up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("test_log.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger()
# logger.info('Downloading new shp version')

# r = requests.get(geo_name_url, stream=True)

# logger.info("Extracting zip contents")
# z = zipfile.ZipFile(io.BytesIO(r.content))
# z.extractall(temp_dir)

logger.info(f"Loading: {file_name}")
data = pd.DataFrame.spatial.from_featureclass(os.path.join(temp_dir, file_name),
                                              sr=spatial_ref)

logger.info("Loading FED_A")
fed_data = pd.DataFrame.spatial.from_featureclass(fed_num_fc, sr=spatial_ref)
fed_data = fed_data[['FED_NUM', 'SHAPE']]
fed_data = fed_data.reindex()
logger.info("Creating Subsets")
for stype in subtypes:
    logger.info(f"Subsetting: {stype}")
    stype_data = data[data[filter_field].isin(subtypes[stype])]
    stype_data = stype_data.reindex()
    # Add spatial join to pointdata subset
    logger.info(f"Creating Spatial Join for {stype}")
    stype_data = stype_data.spatial.join(fed_data, how='left', op='within')

    stype_fc_name = f"{file_name.split('.')[0]}_{stype}"
    logger.info(f'Exporting: {stype_fc_name}')
    stype_data.spatial.to_featureclass(location=os.path.join(output_gdb, stype_fc_name))

logger.info("DONE!")


