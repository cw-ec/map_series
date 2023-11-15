import arcpy
import os
import sys
from components import logging_setup

arcpy.env.overwriteOutput = True  # Needed to overwrite existing outputs


class MapToPDF:
    """Converts all maps in a map series into an individual PDF that is placed in the output directory unsorted"""

    def export_maps(self):
        """Exports the maps as pdfs to the dump directory"""
        # Load the chosen pro project and take the first layout
        p = arcpy.mp.ArcGISProject(self.aprx_path)
        llayouts = p.listLayouts()[0]
        aprx_name = os.path.split(self.aprx_path)[-1]
        # If a layout exists then export the maps
        if not (llayouts.mapSeries is None):
            ms = llayouts.mapSeries
            if ms.enabled:
                # Create a pdf file for each page in the layout
                for pageNum in range(1, ms.pageCount+1):

                    # Build PDF Name for export
                    pfed = ms.pageRow.FED_NUM
                    ptype = aprx_name.split('_')[1][0]
                    num = pageNum

                    if pageNum < 10:
                        num = f"0{pageNum}"

                    pnum = f"{self.map_types[aprx_name.split('_')[2]]}{num}"

                    pdf_name = f"{ptype}_{pfed}_{pnum}"

                    self.logger.info(f'Exporting:{pdf_name}')

                    ms.exportToPDF(os.path.join(self.out_dir, pdf_name),
                                   page_range_type="RANGE",
                                   # Needed to ensure the range of pages we want is used in the export
                                   page_range_string=str(pageNum),  # Exports the specific page we want
                                   resolution=self.dpi,  # DPI of exported maps default is 96 usually set to 300
                                   output_as_image=self.as_image  # As image is needed as some maps will have grey patches if exported as vector graphics
                                   )
                    self.logger.info('Page Exported')

        self.logger.info('DONE!')

    def __init__(self, aprx_path, out_dir, as_image=False, dpi=300):

        # Settable params
        self.aprx_path = aprx_path
        self.out_dir = out_dir
        self.as_image = as_image
        self.dpi = dpi

        # Preset params
        self.map_types = {'OV': '',
                          'SmlInset': 'A',
                          'LrgInset': 'B'
                          }

        # Processing
        self.logger = logging_setup()
        self.logger.info('Export process started')
        self.export_maps()
