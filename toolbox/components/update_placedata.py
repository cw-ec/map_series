import requests
import zipfile
import os
import io
import arcpy
import pandas as pd
import arcgis
from commons import logging_setup, create_verify_gdf
from arcgis.features import GeoAccessor, GeoSeriesAccessor
from arcgis.geometry import SpatialReference


arcpy.env.overwriteOutput = True


class UpdatePlaceNames:

    """
    The purpose of this script is to download the geoplacenames file and then save the subtypes
    (under the 'GENERIC' field) as separate feature classes in a given geodatabase
    """

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
        arcpy.Identity_analysis(os.path.join(self.temp_dir, self.pn_shp_nme),
                                os.path.join(self.temp_gdb, self.cleaned_fed),
                                os.path.join(self.temp_gdb, 'idenitied'),
                                )

    def process(self):
        """Process the imported data and add it to the working database separated into subtypes"""

        self.logger.info("Creating/Verifying existence of essential gdb")
        create_verify_gdf(self.temp_gdb)
        create_verify_gdf(self.output_gdb)

        self.logger.info(f"Loading: {self.pn_shp_nme}")
        data = pd.DataFrame.spatial.from_featureclass(os.path.join(self.temp_dir, self.pn_shp_nme),
                                                      sr=self.spatial_ref)
        self.logger.info("Creating Subsets of placenames data")
        for stype in self.subtypes:
            self.logger.info(f"Sub-setting: {stype}")
            stype_data = data[data[self.filter_field].isin(self.subtypes[stype])]
            stype_data = stype_data.reindex()

            stype_fc_name = f"{self.pn_shp_nme.split('.')[0]}_{stype}"
            self.logger.info(f'Exporting: {stype_fc_name}')
            stype_data.spatial.to_featureclass(location=os.path.join(self.output_gdb, stype_fc_name))

    def is_valid(self, geo_name_fc, output_gdb, fed_num_fc, download_new_data, pn_shp_nme):
        """Validates inputs"""

        if not isinstance(output_gdb, str):
            raise Exception("Parameter 'output_gdb': must be a string")
        if (not isinstance(fed_num_fc, str)) or (not arcpy.Exists(fed_num_fc)):
            raise Exception(f"Parameter 'fed_num_fc': must be a string and must be a path to an existing featureclass or shapefile.")
        if not isinstance(download_new_data, bool):
            raise Exception(f"Parameter 'download_new_data': must be of type boolean")
        if not isinstance(geo_name_fc, str):
            raise Exception(f"Parameter 'geo_name_fc': Must be of type string")
        if not isinstance(pn_shp_nme, str):
            raise Exception("Parameter 'pn_shp_nme': Must be of type string")

    def __init__(self, geo_name_url, output_gdb, fed_num_fc, download_new_data=False, pn_shp_nme="cgn_canada_shp_eng.shp"):

        # Validate inputs
        self.is_valid(geo_name_url, output_gdb, fed_num_fc, download_new_data, pn_shp_nme)
        # Preset Attributes
        self.spatial_ref = '4269'
        self.temp_dir = "..\\..\\data"
        self.temp_gdb = os.path.join(self.temp_dir, 'intermediate.gdb')
        self.filter_field = 'GENERIC'
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
            "Locality": ['Locality'],
            "MetropolitanArea": ['Metropolitan Area']
        }
        self.cleaned_fed = 'cleaned_fed'

        # Attributes with inputs
        self.geo_name_url = geo_name_url
        self.output_gdb = output_gdb
        self.fed_num_fc = fed_num_fc
        self.download_new_data = download_new_data
        self.pn_shp_nme = pn_shp_nme

        # Run Process
        self.logger = logging_setup('.\\')

        # Download the data only if the download_new_data parameter is set to true
        if self.download_new_data:
            self.logger.info("Downloading new version of input dataset")
            self.download_data()

        elif not self.download_new_data:
            self.logger.info("Download_new_data set to False. Subsetting pre-existing dataset")

        self.logger.info("Adding FED Attributes to the Placenames Data")
        self.identity()
        self.logger.info("Processing Data")
        self.process()
        self.logger.info("DONE!")
