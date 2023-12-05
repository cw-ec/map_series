import requests
import zipfile
import sys
import os
import io
import arcpy
import pandas as pd
import arcgis
from toolbox.components import logging_setup, create_verify_gdf
from arcgis.features import GeoAccessor, GeoSeriesAccessor
from arcgis.geometry import SpatialReference
from toolbox.components import configs

arcpy.env.overwriteOutput = True

class UpdatePlaceNames:

    """
    The purpose of this script is to download the geoplacenames file and then save the subtypes (under the generic field) as
    separate featureclasses in a given geodatabase
    """
    def is_valid(self, geo_name_url, out_gdb):
        """Validates inputs and returns an exception is any input is invalid"""
        if not isinstance(geo_name_url, str):
            raise Exception(f"Parameter: geo_name_url must be a valid string and not {type(geo_name_url)}")
        if not isinstance(out_gdb, str):
            raise Exception(f"Parameter: out_gdb must be a string not {type(out_gdb)}")



    def download_data(self):

        """ Downloads a zipfile from a specified source and unzips the contents to the out directory"""

        self.logger.info('Downloading new shp version')

        r = requests.get(self.geo_name_url, stream=True)

        self.logger.info("Extracting zip contents")
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(self.temp_dir)

    def identity(self):
        '''Uses identity to add the fed info to the data'''

        create_verify_gdf(self.temp_gdb)
        # Need to clean the fed data first
        self.logger.info('Cleaning fed data')
        fed_data = pd.DataFrame.spatial.from_featureclass(self.fed_num_fc, sr=self.spatial_ref)
        fed_data = fed_data[['FED_NUM', 'ED_NAMEE', 'ED_NAMEF', 'FedNameLabel', 'ProvEN', 'ProvCode', 'SHAPE']]
        fed_data.spatial.to_featureclass(location=os.path.join(self.temp_gdb, self.cleaned_fed))
        self.logger.info("Running Identity")
        arcpy.Identity_analysis(os.path.join(self.temp_dir, self.file_name),
                                os.path.join(self.temp_gdb, self.cleaned_fed),
                                os.path.join(self.temp_gdb, 'idenitied'),
                                )

    def process(self):
        """Process the imported data and add it to the working database separated into subtypes"""

        self.logger.info("Creating/Verifying existence of essential gdb")
        create_verify_gdf(self.temp_gdb)
        create_verify_gdf(self.output_gdb)

        self.logger.info(f"Loading: {self.file_name}")
        data = pd.DataFrame.spatial.from_featureclass(os.path.join(self.temp_dir, self.file_name),
                                                      sr=self.spatial_ref)
        self.logger.info("Creating Subsets of placenames data")
        for stype in self.subtypes:
            self.logger.info(f"Sub-setting: {stype}")
            stype_data = data[data[self.filter_field].isin(self.subtypes[stype])]
            stype_data = stype_data.reindex()

            stype_fc_name = f"{self.file_name.split('.')[0]}_{stype}"
            self.logger.info(f'Exporting: {stype_fc_name}')
            stype_data.spatial.to_featureclass(location=os.path.join(self.output_gdb, stype_fc_name))

    def __init__(self, geo_name_url, output_gdb, fed_num_fc, download_data=False):

        # Preset Attributes
        self.spatial_ref = '4269'
        self.temp_dir = "..\\data"
        self.temp_gdb = os.path.join(self.temp_dir, 'intermediate.gdb')
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
            "Cities": ['City'],
            "CmptRurComm": ['Compact Rural Community'],
            "Community": ['Community'],
            "Hamlet": ['Hamlet'],
            "Municipality": ['Municipality'],
            "NrthrnComm": ['Northern Community',
                           'Northern Hamlet',
                           'Northern Settlement',
                           'Northern Village',
                           'Northern Village Municipality'
                           ],
            "Parks": ['Amusement Park',
                      'Federal Park',
                      'Industrial Park',
                      'International Park',
                      'Municipal Park',
                      'National Park',
                      'National Park Reserve',
                      'Park',
                      'Provincial Heritage Park',
                      'Provincial Historic Park',
                      'Provincial Marine Park',
                      'Provincial Park',
                      'Provincial Park Reserve',
                      'Provincial Wilderness Park',
                      'Public Park',
                      'Regional Park',
                      'Territorial Park',
                      'Trailer Park'],
            "Resort": ['Resort Municipality',
                       'Resort Village'],
            "SumVil": ['Summer Village'],
            "TownVillage": ['Town',
                            'Village'],
            "UrbComm": ['Urban Community'],
            "Locality": ['Locality']
        }
        self.cleaned_fed = 'cleaned_fed'

        # Attributes with inputs
        self.geo_name_url = geo_name_url
        self.output_gdb = output_gdb
        self.fed_num_fc = fed_num_fc

        # Run Process
        self.logger = logging_setup('.\\')
        self.download_data()
        self.logger.info("Adding FED Attributes to the Placenames Data")
        self.identity()
        self.logger.info("Processing Data")
        self.process()
        self.logger.info("DONE!")
