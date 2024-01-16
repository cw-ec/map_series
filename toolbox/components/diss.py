import os.path

from . import logging_setup, create_verify_gdf
from arcpy.management import Dissolve
import os

from arcpy import env

env.overwriteOutput = True


class DissolveData:

    def dissolver(self):
        """Take the input data and dissolve it by the input field(s)"""
        self.logger.info("Starting Dissolve")
        if len(self.diss_fields) > 0:
            for f in self.diss_fields:
                out_fc_nme = f"{f}"
                self.logger.info(f"Creating dissolve on {f}")
                out_path = os.path.join(self.out_gdb, out_fc_nme)
                Dissolve(in_features=self.in_data,
                         out_feature_class=out_path,
                         dissolve_field=f)
                self.logger.info(f" Dissolve complete {out_fc_nme} created")
        else:
            self.logger.info("Dissolving input dataset by itself as no dissolution fields given")
            Dissolve(in_features=self.in_data,
                     out_feature_class= os.path.join(self.out_gdb, os.path.split(self.in_data)[-1]))

    def is_valid(self, in_data, out_gdb, diss_fields):
        """Validates given inputs before they are set"""
        if not isinstance(in_data, str):
            raise Exception("Parameter 'in_data': Must be of type string")
        if not isinstance(out_gdb, str):
            raise Exception("Parameter 'out_gdb': Must be of type string")
        if not isinstance(diss_fields, list) and not isinstance(diss_fields, list):
            raise Exception("Parameter 'diss_fields': must of of type tuple or list")

    def __init__(self, in_data, out_gdb, diss_fields=("ADV_UID", "SITE_AREA_UID")):

        self.logger = logging_setup()

        # Validate inputs before they are set
        self.logger.info('Validating Inputs')
        self.is_valid(in_data, out_gdb, diss_fields)

        self.in_data = in_data
        self.out_gdb = out_gdb
        self.diss_fields = diss_fields

        # Prep_Data
        self.logger.info("Setting up output geodatabase")
        create_verify_gdf(out_gdb)

        # Process
        self.logger.info(f"Running dissolver on {len(self.diss_fields)} fields")
        self.dissolver()

        self.logger.info("Processing complete")
