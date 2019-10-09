import glob
import logging
import os
import shutil

console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
LOG = logging.getLogger("Cleanup")
LOG.addHandler(console)
LOG.setLevel(logging.INFO)


def cleanup():
    """
    Creates folders for all file types and move the respective files into them

    """
    LOG.info('Cleaning up files')

    file_directories_extensions = [('cif_files', 'cif'),
                                   ('pdb_files', 'pdb'),
                                   ('mol2_files', 'mol2'),
                                   ('charge_files', 'yaml'),
                                   ('ligand_id_files', 'ids'),
                                   ('distances_files', 'distances')]

    for file_format in file_directories_extensions:
        if not os.path.exists(file_format[0]):
            os.mkdir(file_format[0])
        files_to_move = glob.glob(f'./*{file_format[1]}')
        for file in files_to_move:
            file_name = file.split('/')[-1]
            shutil.move(os.path.join(os.getcwd(), file_name),
                        os.path.join(os.getcwd() + f'/{file_format[0]}', file_name))
