import sys
import PyPDF2
import glob
import os
import errno
import logging
from pathlib import Path
from shutil import copyfile


class MapPdfSort:

    """
    Takes the dump directory from the map series and organizes it according to the map series file structure
    """

    def loggingSetup(self):
        # Sets up logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("test_log.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        return logging.getLogger()

    def map_sorting(self):
        """
        Takes the pdfs in the input folder and copies them to the output folder. Organizes the output based on the
        name of the pdf.
        """

        root = Path(self.ddir)
        # Iterate over the map pdf docs and sort them into the folder structure
        for file in root.glob("*.pdf"):

            ptype = file.name.split('_')[0]
            fed = file.name.split('_')[1]
            suffix = file.name.split('_')[2]

            # Add a 0 for sorting purposes if the suffix of the file name looks like this: 'A1' -> 'A01'
            if (suffix.split('.')[0][0].isalpha()) and (len(suffix.split('.')[0]) == 2):
                suffix = f"{suffix.split('.')[0][0]}0{suffix.split('.')[0][1]}"

            out_pdf_path = os.path.join(self.sdir, fed, self.poll_type[ptype])
            # Make sure output path exists. Create if needed
            Path(out_pdf_path).mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Sorting: {file.name}")
            copyfile(os.path.join(root, file.name), os.path.join(out_pdf_path, f"{ptype}_{fed}_{suffix}.pdf"))

    def consolidate_maps(self, subfolders=('ADV', 'PollDay'), combo_name='consolidated'):
        """Consolidates all pdf maps in a given directory and subdirectories into one master file per (sub)directory"""

        def silent_remove(filename):
            try:
                os.remove(filename)
            except OSError as e:  # this would be "except OSError, e:" before Python 2.6
                if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
                    raise  # re-raise exception if a different error occurred

        # Subdirectories in the input directory are expected to be FED numbers in keeping with the folder structure
        for fed in os.listdir(self.sdir):

            root = os.path.join(self.sdir, fed)

            for f in subfolders:

                self.logger.info(f"Consolidating PDFs for FED: {fed} Folder: {f}")
                c_root = os.path.join(root, f)
                to_merge = glob.glob(os.path.join(c_root, '*.pdf'))

                # Merge and export the combined pdf files
                merger = PyPDF2.PdfMerger()
                combo_ext = f'{f}{combo_name}.pdf'
                for pdf in to_merge:
                    # Don't want to combine prior combo pdfs
                    if os.path.split(pdf)[-1] == combo_ext:
                        continue
                    merger.append(pdf)

                out_path = os.path.join(c_root, combo_ext)
                silent_remove(out_path) # Remove the consolidated pdf if it already exists
                merger.write(out_path)
                merger.close()

    def __init__(self, dump_dir, sorted_dir) -> None:

        self.logger = self.loggingSetup()
        self.logger.info(f"Sorting all PDF maps in: {dump_dir}")
        # Set Class Vars
        self.poll_type = {'A': 'ADV',
                          'P': 'PollDay'}

        self.ddir = dump_dir
        self.sdir = sorted_dir

        # Run process
        self.logger.info("Sorting maps in input directory")
        self.map_sorting()

        self.logger.info("Consolidating maps in designated folders")
        self.consolidate_maps()
        self.logger.info("DONE!")


if __name__ == '__main__':
    # Config for testing
    sdir = r"C:\map_series\data\MS_ExportedMaps\sorted"
    ddir = r"C:\map_series\data\MS_ExportedMaps\Dump_AllMaps"

    MapPdfSort(dump_dir=ddir, sorted_dir=sdir) # Test Call




