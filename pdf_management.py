import sys
import PyPDF2
import glob
import os
import errno
import logging
from pathlib import Path
from shutil import copyfile
# ------------------------------------
# Inputs

ddir = r'C:\map_series\data\MS_ExportedMaps\Dump_AllMaps'
sdir = r'C:\map_series\data\MS_ExportedMaps\sorted'

# -----------------------------------


class MapPdfSort:

    """
    Takes the dump directory from the map series and organizes it according to the map series file structure
    """

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

            out_pdf_path = os.path.join(self.sdir, fed, self.poll_type[ptype])
            # Make sure output path exists. Create if needed
            Path(out_pdf_path).mkdir(parents=True, exist_ok=True)
            logger.info(f"Sorting: {file.name}")
            copyfile(os.path.join(root, file.name), os.path.join(out_pdf_path, file.name))

    def consolidate_maps(self, combo_name='combined'):
        '''Consolidates all pdf maps in a given folder into one master file'''

        def silentremove(filename):
            try:
                os.remove(filename)
            except OSError as e:  # this would be "except OSError, e:" before Python 2.6
                if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
                    raise  # re-raise exception if a different error occurred

        combo_ext = f'{combo_name}.pdf'

        for fed in os.listdir(self.sdir):
            root = os.path.join(sdir, fed)
            for f in ['ADV', 'PollDay']:
                croot = os.path.join(root, f)
                to_merge = glob.glob(os.path.join(croot, '*.pdf'))

                # Merge and export the combined pdf files
                merger = PyPDF2.PdfMerger()
                for pdf in to_merge:
                    # Don't want to combine prior combo pdfs
                    if os.path.split(pdf)[-1] == combo_ext:
                        continue
                    merger.append(pdf)
                out_path = os.path.join(croot, combo_ext)
                silentremove(out_path)
                merger.write(out_path)
                merger.close()

    def __init__(self, dump_dir, sorted_dir) -> None:

        logger.info(f"Sorting all PDF maps in: {dump_dir}")
        # Set Class Vars
        self.poll_type = {'A': 'ADV',
                          'P': 'PollDay'}

        self.ddir = dump_dir
        self.sdir = sorted_dir

        # Run process
        logger.info("Sorting maps in input directory")
        self.map_sorting()
        logger.info("Consolidating maps in designated folders")
        self.consolidate_maps()


if __name__ == '__main__':
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
    MapPdfSort(r"C:\map_series\data\MS_ExportedMaps\Dump_AllMaps", sorted_dir=sdir)




