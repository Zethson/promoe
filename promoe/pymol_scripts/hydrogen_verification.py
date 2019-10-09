import itertools
import logging
import re
from sys import argv

from pymol import cmd

console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
LOG = logging.getLogger("Hydrogen Verification")
LOG.addHandler(console)
LOG.setLevel(logging.INFO)


# mol 2 file format specifications taken from
# http://chemyang.ccnu.edu.cn/ccb/server/AIMMS/mol2.pdf

class Distance:
    def __init__(self,
                 source_chain,
                 source_atom_id,
                 target_chain,
                 target_atom_id,
                 distance):
        self.source_chain = source_chain
        self.source_atom_id = source_atom_id,
        self.target_chain = target_chain
        self.target_atom_id = target_atom_id,
        self.distance = distance


def parse_distances(distances_file):
    """
    Parses all distances and returns an internal representation for the distances.

    :param distances_file: Path to the distances file.
    :return: List of Distances
    """
    with open(distances_file, 'r') as f: content = f.readlines()

    all_distances = []
    for line in content:
        chains = list(map(lambda chain: chain.replace('\'', ''), re.findall("'.+?'", line)))
        source_chain = chains[0]
        target_chain = chains[1]
        atom_ids = list(map(float, re.findall(r"\d+(?:\.\d+)?", "".join(re.findall(", [0-9]+\)", line)))))
        source_atom_id = int(atom_ids[0])
        target_atom_id = int(atom_ids[1])
        distance = re.findall("[0-9]+\.\d+(?=\D*$)", line)[0]

        all_distances.append(Distance(source_chain, source_atom_id, target_chain, target_atom_id, distance))

    return all_distances


def remove_hydrogens(mol2_file, atoms_to_keep, remove_all):
    """
    Removes water from the mol2 file.

    :param mol2_file: Path to the mol2 file.
    :param atoms_to_keep: List of atomIDs that are within a specific distance to the ligand and should NOT be deleted.
    :param remove_all: If all water atoms should be removed.
    """
    with open(mol2_file, 'r') as f:
        content = f.readlines()
    # first strip everything until @<TRIPOS>ATOM
    molecule_counter = 0
    for line in content:
        molecule_counter += 1
        if line.startswith('@<TRIPOS>ATOM'):
            break
    molecule_less_content = content[molecule_counter:]

    # determine which atoms to delete those are all HOH atoms that are not in the ligand or within distance of less
    # than 4 angstrom (determined by the distance file)
    atoms_to_delete = []
    for line in molecule_less_content:
        if line.startswith('@<TRIPOS>BOND'):
            break
        split = str.split(line)

        current_atom_atom_id = int(str.strip(split[0]))
        current_atom_atom_type = str.strip(split[5])
        current_atom_subst_name = str.strip(split[7])

        if remove_all:
            if (current_atom_atom_type == 'H' or current_atom_atom_type == 'O' or current_atom_atom_type == 'O.3') \
                    and 'HOH' in current_atom_subst_name:
                atoms_to_delete.append(current_atom_atom_id)
        else:
            if (current_atom_atom_type == 'H' or current_atom_atom_type == 'O' or current_atom_atom_type == 'O.3') \
                    and 'HOH' in current_atom_subst_name \
                    and current_atom_atom_id not in atoms_to_keep:
                atoms_to_delete.append(current_atom_atom_id)

    # delete the atoms with the use of pymol
    cmd.reinitialize()
    cmd.load(mol2_file)
    for atom_id in atoms_to_delete:
        cmd.select("atom_to_remove", "id %s" % atom_id)
        cmd.remove("atom_to_remove")

    mol2_name = '.'.join(map(str, mol2_file.split('/')[-1].split('.')[:-1])).replace('.pdb', '')
    cmd.save('%s_no_hydrogens.mol2' % mol2_name, "all")


def remove_selected_hydrogens(mol2, distances, remove_all):
    """
    Entry point for this script. Removes all selected water.

    :param mol2: Path to the mol2 file.
    :param distances: Path to the distances file
    :param remove_all: Boolean whether or not to remove all water
    """
    all_distances = parse_distances(distances)
    atoms_to_keep = list(
        itertools.chain(
            *{atom for atom in sum([(atom.source_atom_id, atom.target_atom_id) for atom in all_distances], ())}))

    remove_hydrogens(mol2, atoms_to_keep, remove_all)


all_argv = argv[1:]
mol2 = all_argv[0]
distances = all_argv[1]
remove_all = all_argv[2]
remove_selected_hydrogens(mol2, distances, remove_all=remove_all)
