# -*- coding: utf-8 -*-

"""Console script for promoe."""
import glob
import itertools
import logging
import os
import subprocess
import sys
import click

from promoe.cleanup import cleanup
from promoe.util.command_util import is_tool_accessible

from promoe.util.list_util import group

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
@click.option(
    '--pdbs',
    multiple=True,
    required=True,
)
def protonize(pdbs):
    LOG.info('Protonize')

    # extract ligands and binding sites
    for pdb in pdbs:
        LOG.info(f'Extracting ligands and binding sites for {pdb}')
        subprocess.run(['pymol', '-qrc', f'{WD}/pymol_scripts/extract_ligands.py', '--', f'{pdb}'])

    # extract all alternative locations of atoms
    pdb_files = glob.glob('*.pdb')
    for pdb in pdb_files:
        LOG.info(f'Extracting alternative locations for {pdb}')
        subprocess.run(['python', f'{WD}/pymol_scripts/altloc_extraction.py', '--pdb', pdb])

    # protonizing
    pdb_files = glob.glob('*.pdb')
    for pdb in pdb_files:
        LOG.info(f'Protonizing {pdb}')
        subprocess.run(['bash', f'{WD}/svl_scripts/run_protonate.sh', f'{WD}/svl_scripts/protonate.svl', pdb])

    # convert all pdb files to mol2
    pdb_files = glob.glob('*.pdb')
    for pdb in pdb_files:
        LOG.info(f'Converting pdb file to mol2 for {pdb}')
        subprocess.run(
            ['bash', f'{WD}/svl_scripts/run_pdb_convertion.sh', f'{WD}/svl_scripts/convert_pdb_mol2.svl', pdb])

    # extract charges
    mol_2_files = glob.glob('*.mol2')
    for mol2 in mol_2_files:
        LOG.info(f'Extracting charges for {mol2}')
        subprocess.run(['python', f'{WD}/pymol_scripts/extract_charges.py', '--mol2', mol2])

    cleanup()


@promoe_cli.command()
@click.option(
    '--pdb',
    nargs=1,
    required=True
)
@click.option(
    '--atoms',
    multiple=True,
    required=True
)
@click.option(
    '--chain',
    required=False
)
def protonize_selected(pdb, atoms, chain='all'):
    # promoe protonize-selected --pdb /home/xb/PycharmProjects/promoe/pdb_files/4agl_full.pdb --atoms '[\'GLN\', \'144\', \'N\'], [\'LEU\', \'145\', \'N\']' --chain A
    result = list(group(atoms, ']'))
    atoms = list(itertools.chain.from_iterable(result))[0]

    if chain is 'all':
        LOG.info(f'Protonizing selected atoms for {pdb}')
        subprocess.run(['bash',
                        f'{WD}/svl_scripts/run_choose_atoms.sh',
                        f'{WD}/svl_scripts/choose_atoms.svl',
                        pdb,
                        atoms])
    else:  # chain A or B
        LOG.info(f'Extracting chain {chain} for {pdb}')
        subprocess.run(['pymol', '-qrc', f'{WD}/pymol_scripts/extract_chains_only.py', '--', pdb, chain])
        pdb_chain_file = "%s_chain_%s.pdb" % (pdb.split('/')[-1][:-4], chain)
        LOG.info(f'Protonizing selected atoms of {chain} for {pdb}')
        subprocess.run(['bash',
                        f'{WD}/svl_scripts/run_choose_atoms.sh',
                        f'{WD}/svl_scripts/choose_atoms.svl',
                        pdb_chain_file,
                        atoms])

    cleanup()

@promoe_cli.command()
@click.option(
    '--mol2',
    required=True
)
@click.option(
    '--keep_hydrogens/--remove_hydrogens',
    default=False
)
@click.option(
    '--distance',
    default=4
)
def clean_hydrogens(mol2, keep_hydrogens, distance):
    if not keep_hydrogens:
        subprocess.run(['pymol', '-qrc', f'{WD}/pymol_scripts/extract_distances.py', '--', mol2])
    # TODO THIS IS NOT YET FINISHED




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
