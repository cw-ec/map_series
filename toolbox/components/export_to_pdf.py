import arcpy
import os
import sys
import glob
import pandas as pd
from arcgis.features import GeoAccessor, GeoSeriesAccessor
from arcgis.geometry import SpatialReference
from . import logging_setup, create_dir

arcpy.env.overwriteOutput = True  # Needed to overwrite existing outputs


class MapToPDF:
    """Converts all maps in a map series into an individual PDF that is placed in the output directory unsorted"""

    def export_maps(self):
        """Exports the maps as pdfs to the dump directory"""
        # Load the chosen pro project and take the first layout
        p = arcpy.mp.ArcGISProject(self.aprx_path)
        llayouts = p.listLayouts()[0]
        # If a layout exists then export the maps
        if not (llayouts.mapSeries is None):
            ms = llayouts.mapSeries
            if ms.enabled:
                # Create a pdf file for each page in the layout
                index_df = pd.DataFrame.spatial.from_featureclass(ms.indexLayer.dataSource)
                for pageNum in index_df['PageCode'].values.tolist():

                    try:
                        ms.currentPageNumber = pageNum  # Set the active map
                    except ValueError:
                        # In some cases there are pages in the list that are not in the map series we are working with in those cases skip them
                        continue

                    self.logger.info(f"Exporting: {pageNum}")
                    # Set PDF Name for export
                    pdf_name = pageNum  # Set the name here incase edits are needed in the future
                    ms.exportToPDF(os.path.join(self.out_dir, pdf_name),
                                   page_range_type="CURRENT",
                                   #page_range_string=f'{pageNum}',
                                   resolution=self.dpi,  # DPI of exported maps default is 96 usually set to 300
                                   output_as_image=self.as_image
                                   # As image is needed as some maps will have grey patches if exported as vector graphics
                                   )
                    self.logger.info('PDF Exported')

        self.logger.info('DONE!')

    def is_valid(self, aprx_path, out_dir, as_image, dpi, page_number_field_name):
        """Validates class inputs"""
        if not isinstance(aprx_path, str):
            raise Exception("Parameter 'aprx_path' must be a string")
        if not isinstance(out_dir, str):
            raise Exception("Parameter 'out_dir' must be a string")
        if not isinstance(as_image, bool):
            raise Exception("Parameter 'as_image' must be a boolean")
        if not isinstance(dpi, int):
            raise Exception("Parameter 'dpi' must be an integer")
        if not isinstance(page_number_field_name, str):
            raise Exception(f"Parameter 'page_number_field_name' must be of type string")

    def __init__(self, aprx_path, out_dir, as_image=False, dpi=150, page_number_field_name="PageCode"):

        # Validate inputs
        self.is_valid(aprx_path, out_dir, as_image, dpi, page_number_field_name)

        # Settable params
        self.aprx_path = aprx_path
        self.out_dir = out_dir
        self.as_image = as_image
        self.dpi = dpi
        self.pg_nbr_fld_nme = page_number_field_name

        # Processing
        self.logger = logging_setup()
        self.logger.info('Export process started')
        create_dir(self.out_dir)
        self.export_maps()


class BulkMapToPDF:
    """Bulk version of MapToPDF class allows for multiple aprx files to be exported into pdf files at once"""

    def is_valid(self, in_dir, out_dir, to_pdf_list, as_image, dpi, page_number_field_name):
        """checks class inputs to see if they are valid, Raise exception if not"""

        if not isinstance(in_dir, str):
            raise Exception("Parameter 'in_dir' must be a string")
        if not isinstance(out_dir, str):
            raise Exception("Parameter 'out_dir' must be a string")
        if not isinstance(to_pdf_list, tuple) and not isinstance(to_pdf_list, list):
            raise Exception("Parameter: 'to_pdf_list' must a tuple or a list")
        if not isinstance(as_image, bool):
            raise Exception("Parameter 'as_image' but be of type boolean")
        if not isinstance(dpi, int):
            raise Exception("Parameter 'dpi' must be an integer")
        if not isinstance(page_number_field_name, str):
            raise Exception(f"Parameter 'page_number_field_name' must be of type string")

    def bulk_export(self):
        """Bulk exports input list of aprx files into pdfs"""
        # Make the list of aprx files in the given directory and subdirectories
        aprx_list = glob.glob(os.path.join(self.in_dir, '**\\*.aprx'), recursive=True)

        # If the pdf list param is populated then filter the list to only include file names that appear in the list
        if len(self.to_pdf_list) > 0:
            aprx_list = [a for a in aprx_list if os.path.split(a)[-1] in self.to_pdf_list]

        if len(aprx_list) > 0:
            for aprx in aprx_list:
                self.logger.info(f"Exporting aprx {aprx_list.index(aprx)+1} of {len(aprx_list)}: {os.path.split(aprx)[-1]}")
                MapToPDF(aprx, self.out_dir, dpi=self.dpi, page_number_field_name=self.pg_nbr_fld_nme)

        else:
            self.logger.info(f"Number of available aprx files that match input criteria == 0. Please check inputs and try again.")
            sys.exit()

    def __init__(self, in_dir, out_dir, to_pdf_list=(), as_image=False, dpi=150, page_number_field_name="PageCode"):

        # Validate Inputs
        self.is_valid(in_dir, out_dir, to_pdf_list, as_image, dpi, page_number_field_name)

        # Set Inputs
        self.in_dir = in_dir
        self.out_dir = out_dir
        self.to_pdf_list = to_pdf_list
        self.as_image = as_image
        self.dpi = dpi
        self.pg_nbr_fld_nme = page_number_field_name

        self.logger = logging_setup()

        self.logger.info(f"Starting bulk export of {self.in_dir}")
        self.bulk_export()
        self.logger.info("Bulk Export Complete!")
