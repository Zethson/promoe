import logging
import os
import click

from Bio.PDB import *

console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
LOG = logging.getLogger("Extract Altloc")
LOG.addHandler(console)
LOG.setLevel(logging.INFO)


class NotDisorderedA(Select):
    """
    Implements select interface of pymol.
    Accepts all atoms, which are in altloc A
    """
    def accept_atom(self, atom):
        return not atom.is_disordered() or atom.get_altloc() == 'A'


class NotDisorderedB(Select):
    """
    Implements select interface of pymol
    Accepts all atoms, which are in altloc B
    """
    def accept_atom(self, atom):
        return not atom.is_disordered() or atom.get_altloc() == 'B'


@click.command()
@click.option('-p', '--pdb',
              help='path to pdb file',
              required=True)
def extract_altlocs(pdb):
    """
    Extracts the alternative locations of atoms in a pdb file and saves it.
    Alternative locations are determined via the disordered property of the atoms in the PDB file.
    Sideeffect: the input PDB file is deleted! It is replaced by the altloc pdb(s).

    :param pdb: path to the pdb file
    """
    parser = PDBParser()
    pdb_id = pdb.split('_')[0]
    structure = parser.get_structure(pdb_id, pdb)
    IO = PDBIO()

    # if any disordered atoms are in the pdb file
    # -> extract only the non-disordered atoms with the respective disordered atoms (A or B)
    # replace the original pdb file with 2 pdb files containing the altlocs
    atoms = structure.get_atoms()
    disordered_atoms = list(filter(lambda atom: atom.occupancy < 1, atoms))
    if disordered_atoms:
        IO.set_structure(structure)
        if not 'full' in pdb:
            # binding site or ligand
            altloc_prefix = pdb.split('_')[:4]
            altloc_suffix = pdb.split('_')[4:]
            IO.save('_'.join(altloc_prefix) + '_altloc_A_' + '_'.join(altloc_suffix), select=NotDisorderedA())
            IO.save('_'.join(altloc_prefix) + '_altloc_B_' + '_'.join(altloc_suffix), select=NotDisorderedB())
            if os.path.exists(pdb):
                os.remove(pdb)
            else:
                LOG.error(f'File {pdb} was not found during cleanup! Unable to delete file {pdb}.')


if __name__ == '__main__':
    extract_altlocs()
