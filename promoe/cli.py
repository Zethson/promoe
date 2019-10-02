# -*- coding: utf-8 -*-

"""Console script for promoe."""
import glob
import logging
import os
import shutil
import subprocess
import sys
import click

from promoe.util.command_util import is_tool_accessible
from shlex import quote

WD = os.path.dirname(__file__)

console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
LOG = logging.getLogger("Promoe")
LOG.addHandler(console)
LOG.setLevel(logging.INFO)


@click.group()
@click.option(
    '-v', '--verbose',
    is_flag=True,
    default=False,
    help="Verbose output (print debug statements)"
)
def promoe_cli(verbose):
    if verbose:
        logging.basicConfig(level=logging.DEBUG, format="\n%(levelname)s: %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="\n%(levelname)s: %(message)s")


@promoe_cli.command()
@click.argument(
    'pdbs',
    nargs=-1,
    required=True,
)
def protonize(pdbs):
    LOG.info('Protonize')

    pdbs = pdbs[1:]
    # extract ligands and binding sites
    for pdb in pdbs:
        LOG.info(f'Extracting ligands and binding sites for {pdb}')
        subprocess.run(['pymol', '-qrc', WD + '/pymol_scripts/extract_ligands.py', '--', f'{pdb}'])

    # extract all alternative locations of atoms
    pdb_files = glob.glob('*.pdb')
    for pdb in pdb_files:
        LOG.info(f'Extracting alternative locations for {pdb}')
        subprocess.run(['python', WD + '/pymol_scripts/altloc_extraction.py', '--pdb', pdb])

    # convert all pdb files to mol2
    pdb_files = glob.glob('*.pdb')
    for pdb in pdb_files:
        LOG.info(f'Converting pdb file to mol2 for {pdb}')
        subprocess.run(['bash', WD + '/svl_scripts/run_pdb_convertion.sh', WD + '/svl_scripts/convert_pdb_mol2.svl', pdb])

    cleanup()


def cleanup():
    LOG.info('Cleaning up files')

    file_directories_extensions = [('cif_files', 'cif'),
                                   ('pdb_files', 'pdb'),
                                   ('mol2_files', 'mol2'),
                                   ('charge_files', 'yaml'),
                                   ('ligand_id_files', 'ids')]

    for file_format in file_directories_extensions:
        if not os.path.exists(file_format[0]):
            os.mkdir(file_format[0])
        files_to_move = glob.glob(f'./*{file_format[1]}')
        for file in files_to_move:
            file_name = file.split('/')[-1]
            shutil.move(os.path.join(os.getcwd(), file_name), os.path.join(os.getcwd() + f'/{file_format[0]}', file_name))


def main():
    """
    Main entry point for Promoe
    """

    print('''                 ____  ____   ___  __  __  ___  _____
                |  _ \|  _ \ / _ \|  \/  |/ _ \| ____|
                | |_) | |_) | | | | |\/| | | | |  _|
                |  __/|  _ <| |_| | |  | | |_| | |___
                |_|   |_| \_ \\___/|_|  |_|\___/|_____|''')

    LOG.info('Trying to detect MOE...')
    if is_tool_accessible('moebatch'):
        LOG.info('MOE successfully detected!')
    else:
        LOG.error('MOE could not be detected via \'moebatch\'! Aborting...')
        sys.exit(1)

    LOG.info('Trying to detect Pymol...')
    if is_tool_accessible('pymol'):
        LOG.info('Pymol successfully detected')
    else:
        LOG.error('Pymol could not be detected via \'pymol\' Aborting...')
        sys.exit(1)

    promoe_cli()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
