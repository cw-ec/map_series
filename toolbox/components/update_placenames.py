import requests
import zipfile
import sys
import os
import io
import arcpy
import pandas as pd
import arcgis
from components import logging_setup
from arcgis.features import GeoAccessor, GeoSeriesAccessor
from arcgis.geometry import SpatialReference

"""
The purpose of this script is to download the geoplacenames file and then save the subtypes (under the generic field) as 
separate featureclasses in a given geodatabase
"""


class UpdatePlaceNames:

    def download_data(self):

        """ Downloads a zipfile from a specified source and unzips the contents to the out directory"""

        self.logger.info('Downloading new shp version')

        r = requests.get(self.geo_name_url, stream=True)

        self.logger.info("Extracting zip contents")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(self.temp_dir)

    def process(self):
        """Process the imported data and add it to the working database separated into subtypes"""

        self.logger.info(f"Loading: {self.file_name}")
        data = pd.DataFrame.spatial.from_featureclass(os.path.join(self.temp_dir, self.file_name),
                                                      sr=self.spatial_ref)

        self.logger.info("Loading FED_A")
        fed_data = pd.DataFrame.spatial.from_featureclass(self.fed_num_fc, sr=self.spatial_ref)
        fed_data = fed_data[['FED_NUM', 'SHAPE']]
        fed_data = fed_data.reindex()
        self.logger.info("Creating Subsets")
        for stype in self.subtypes:
            self.logger.info(f"Sub-setting: {stype}")
            stype_data = data[data[self.filter_field].isin(self.subtypes[stype])]
            stype_data = stype_data.reindex()
            # # Add spatial join to pointdata subset
            # self.logger.info(f"Creating Spatial Join for {stype}")
            # stype_data = stype_data.spatial.join(fed_data, how='left', op='within')

            stype_fc_name = f"{self.file_name.split('.')[0]}_{stype}"
            self.logger.info(f'Exporting: {stype_fc_name}')
            stype_data.spatial.to_featureclass(location=os.path.join(self.output_gdb, stype_fc_name))

    def __init__(self, geo_name_url, output_gdb, fed_num_fc):

        # Preset Attributes
        self.spatial_ref = '4269'
        self.temp_dir = r"C:\map_series_tests\data"
        self.filter_field = 'GENERIC'
        self.file_name = "cgn_canada_shp_eng.shp"
        self.subtypes = {
            'Airport': ['Airport',
                        'Airfield'
                        ],
            'CFB': ['Canadian Forces Base',
                    'Canadian Forces Camp',
                    'Canadian Forces Range and/or Training Area (C.F.T.A.)',
                    'Canadian Forces Station'
                    ],
            "Cities": [],
            "CmptRurComm": [],
            "Community": [],
            "Hamlet": [],
            "Municipality": [],
            "NrthrnComm": [],
            "Parks": [],
            "Resort": [],
            "SumVil": [],
            "TownVillage": [],
            "UrbComm": []
        }

        # Attributes with inputs
        self.geo_name_url = geo_name_url
        self.output_gdb = output_gdb
        self.fed_num_fc = fed_num_fc
        # Run Process
        self.logger = logging_setup('.\\')
        # self.download_data()
        self.process()
