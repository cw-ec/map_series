import sys
import PyPDF2
import glob
import os
import errno
from pathlib import Path
from shutil import copyfile, rmtree, make_archive
from . import logging_setup


class MapPdfSort:

    """
    Takes the dump directory from the map series and organizes it according to the map series file structure
    """

    def map_sorting(self):
        """
        Takes the pdfs in the input folder and copies them to the output folder. Organizes the output based on the
        name of the pdf.
        """

        def zip_folders(outdir, fedlist: list) -> None:
            """Zips all fed folders that were just processed, delete the old folder structure"""

            for fed in list(set(fedlist)):
                self.logger.info(f" Zipping: {fed}")
                fed_path = Path(os.path.join(outdir, fed))
                if os.path.exists(fed_path):
                    make_archive(str(fed_path), 'zip', root_dir=fed_path)
                    self.logger.info(f" Deleting original directory for {fed}")
                    if os.path.exists(fed_path):
                        rmtree(fed_path)

        root = Path(self.ddir)
        # Iterate over the map pdf docs and sort them into the folder structure
        fed_list = []
        pdf_list = list(root.glob("*.pdf"))  # Create the list of pdf files in the dump directory

        # If there are no pdf files don't both sorting the empty list
        if len(pdf_list) == 0:
            self.logger.info(f"No PDF files found in {self.ddir}. Please check 'dump_dir' parameter.")
            sys.exit()

        self.logger.info(f"Sorting {len(pdf_list)} pdfs")
        for file in pdf_list:
            ptype = file.name.split('_')[0]
            fed = file.name.split('_')[0].split('.')[0]

            # For those inset index cases.
            if not fed.isdigit():
                fed = file.name.split('_')[-1].split('.')[0]
                if not fed.isdigit():  #  If value is still not numeric after this return warning and continue
                    self.logger.warning(f"{file.name} does not fit the naming convention for sorting. Skipping file.")
                    continue

            if fed not in fed_list:
                fed_list.append(fed)

            if (ptype == 'InsetIndex') or (ptype == 'IndexCartons'):  # no suffix on inset reports use simplified workflow

                out_pdf_path = os.path.join(self.sdir, fed)

                Path(out_pdf_path).mkdir(parents=True, exist_ok=True)
                self.logger.info(f"Sorting: {file.name}")
                copyfile(os.path.join(root, file.name), os.path.join(out_pdf_path, f"{file.name}"))

            else:  # Map PDF's have more components and need a more complex workflow
                suffix = file.name.split('_')[-1].split('.')[0]

                # Add a 0 for sorting purposes if the suffix of the file name looks like this: 'A1' -> 'A01'
                if (suffix.split('.')[0][0].isalpha()) and (len(suffix) == 2):
                    suffix = f"{suffix[0]}0{suffix[1]}"

                # Folder names differ by province
                if (int(fed) >= 24000) and (int(fed) < 25000):  # Quebec
                    subdir = 'cartes_maps'
                else:  # RoC
                    subdir = 'maps_cartes'

                out_pdf_path = os.path.join(self.sdir, fed, subdir)
                # Make sure output path exists. Create if needed
                Path(out_pdf_path).mkdir(parents=True, exist_ok=True)
                self.logger.info(f"Sorting: {file.name}")
                copyfile(os.path.join(root, file.name), os.path.join(out_pdf_path, f"{fed}_{suffix}.pdf"))

        self.logger.info("Zipping all dumped files")
        # Zip all the folders that were just processed
        zip_folders(outdir=self.sdir, fedlist=fed_list)


    def is_valid(self, dump_dir, sorted_dir):
        """Validates class inputs"""
        if not isinstance(dump_dir, str):
            raise Exception("Input dump_dir must be a string")
        if not isinstance(sorted_dir, str):
            raise Exception("Input sorted_dir must be a string")

    def __init__(self, dump_dir, sorted_dir) -> None:
        # Validate inputs
        self.is_valid(dump_dir, sorted_dir)

        # Create Logger
        self.logger = logging_setup()

        # Set Class Vars
        self.ddir = dump_dir
        self.sdir = sorted_dir

        self.logger.info(f"Sorting all PDF maps in: {self.ddir}")
        self.logger.info(f"All sorted files to be placed in {self.sdir}")

        # Run process
        self.logger.info("Sorting maps in input directory")
        self.map_sorting()

        self.logger.info("DONE!")


class PDFConsolidator:

    def consolidate_maps(self, sub_folders=('ADV', 'PollDay'), combo_name='consolidated'):
        """Consolidates all pdf maps in a given directory and subdirectories into one master file per (sub)directory"""

        def silent_remove(filename):
            try:
                os.remove(filename)
            except OSError as e:
                if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
                    raise  # re-raise exception if a different error occurred

        # Subdirectories in the input directory are expected to be FED numbers in keeping with the folder structure
        for fed in os.listdir(self.in_dir):

            root = os.path.join(self.in_dir, fed)
            combo_dir = f'{fed}_consolidated'
            out_base = os.path.join(root, combo_dir)

            if (len(self.feds_to_consolidate) > 0) and (int(fed) not in self.feds_to_consolidate):
                continue

            for f in sub_folders:

                self.logger.info(f"Consolidating PDFs for FED: {fed} Folder: {f}")
                sub_folder = os.path.join(root, f)
                to_merge = glob.glob(os.path.join(sub_folder, '*.pdf'))

                # Merge and export the combined pdf files
                merger = PyPDF2.PdfFileMerger()
                combo_ext = f'{f}{combo_name}.pdf'
                for pdf in to_merge:
                    # Don't want to combine prior combo pdfs
                    if os.path.split(pdf)[-1] == combo_ext:
                        continue
                    merger.append(pdf)

                # Export the consolidated pdf
                out_path = os.path.join(out_base, combo_ext)
                Path(out_base).mkdir(parents=True, exist_ok=True)
                silent_remove(out_path)  # Remove the consolidated pdf if it already exists
                merger.write(out_path)
                merger.close()

            make_archive(os.path.join(self.out_dir, str(fed)), 'zip', root_dir=out_base)
            if os.path.exists(out_base):
                rmtree(out_base)

    def is_valid(self, in_dir, feds_to_combo):
        """Validates Inputs"""
        if not isinstance(in_dir, str):
            raise Exception("in_dir must be a string")
        if not isinstance(feds_to_combo, tuple) and not isinstance(feds_to_combo, list):
            raise Exception("feds_to_combo must be either a list or tuple")

    def __init__(self, in_dir, feds_to_combo=tuple()):

        # Validate inputs
        self.is_valid(in_dir, feds_to_combo)

        # Settable Inputs
        self.in_dir = in_dir
        self.feds_to_consolidate = feds_to_combo

        # Set output directory at root level of input directory
        self.out_dir = os.path.join(self.in_dir, 'consolidated')

        # Setup Logging and Run the process
        self.logger = logging_setup()
        self.consolidate_maps()


if __name__ == "__main__":

    PDFConsolidator(
        in_dir=".\\data\\sorted",
        # feds_to_combo=[24002, 24013]
    )


