import logging
import tqdm
from _decimal import Decimal
from dataclasses import dataclass
import yaml

import click as click

console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
LOG = logging.getLogger("Extract Charges")
LOG.addHandler(console)
LOG.setLevel(logging.INFO)


# mol 2 file format specifications taken from
# http://chemyang.ccnu.edu.cn/ccb/server/AIMMS/mol2.pdf
@dataclass
class Residue:
    atoms: []


@dataclass
class Atom:
    atom_id: int
    atom_name: str
    x_coord: Decimal
    y_coord: Decimal
    z_coord: Decimal
    atom_type: str
    subst_id: int
    subst_name: str
    charge: Decimal
    status_bit: str


@click.command()
@click.option('-m', '--mol2',
              help='Path to mol2 file',
              required=True)
def extract_charges(mol2):
    """
    Extracts the charges of all residues and also sums them up for the total charge.

    :param mol2: Path to the mol2 file
    """
    all_residues = parse_mol2(mol2)
    all_charges_per_residue = list(map(lambda residue: sum(map(lambda atom: atom.charge, residue.atoms)), all_residues))
    total_charge = sum(all_charges_per_residue)

    write_charges(all_residues, all_charges_per_residue, total_charge, mol2)


def parse_mol2(mol2):
    """
    Parses a mol2 file for the required downstream information.

    :param mol2: Path to the mol2 file
    :return: list of Residues
    """
    with open(mol2, 'r') as f:
        lines = f.readlines()
        try:
            tripos_atom_idx = lines.index('@<TRIPOS>ATOM\n')
            tripos_bond_idx = lines.index('@<TRIPOS>BOND\n')
        except ValueError:
            LOG.error(f'Unable to find @<TRIPOS>ATOM or @<TRIPOS>BOND record in file {mol2}')
        atom_records_only = lines[tripos_atom_idx + 1:tripos_bond_idx]

        # reconstruct residues -> move from N atom_name to N atom_name
        all_residues = []
        new_residue = Residue([])
        for record in tqdm.tqdm(atom_records_only):
            # new residue
            if record[4] == 'N' and not str.strip(record[5]):
                if new_residue.atoms:
                    all_residues.append(new_residue)
                    new_residue = Residue([])

            split = str.split(record)
            # missing status_bit? -> insert dummy
            if len(split) < 10:
                split.append('-')

            current_atom = Atom(atom_id=int(str.strip(split[0])),
                                atom_name=str.strip(split[1]),
                                x_coord=Decimal(split[2]),
                                y_coord=Decimal(split[3]),
                                z_coord=Decimal(split[4]),
                                atom_type=str.strip(split[5]),
                                subst_id=int(str.strip(split[6])),
                                subst_name=str.strip(split[7]),
                                charge=Decimal(str.strip(split[8])),
                                status_bit=str.strip(split[9]))

            new_residue.atoms.append(current_atom)

        all_residues.append(new_residue)

        return all_residues


def write_charges(all_residues, all_charges_per_residue, total_charge, mol2):
    """
    Writes the charges file. Name of the output file will be determined by the name of the input mol2 file.

    :param all_residues: List of Residues
    :param all_charges_per_residue: List of charges per Residue
    :param total_charge: Integer number of total charge
    :param mol2: Path to the original mol2 file
    """
    # solely all subst_names
    all_residue_subst_name = list(map(lambda residue: residue.atoms[0].subst_name, all_residues))
    # solely float numbers of charges (as strings)
    all_charges_per_residue = list(map(lambda charge: str(charge), all_charges_per_residue))

    # setup yaml structure
    formatted_yaml_output = {'file': mol2, 'total_charge': str(total_charge),
                             'residues': dict(zip(all_residue_subst_name, all_charges_per_residue))}

    # dump to yaml
    with open(str.split(mol2, '/')[-1] + '_charges.yaml', 'w') as yaml_file:
        yaml.dump(formatted_yaml_output, yaml_file, default_flow_style=False)


if __name__ == '__main__':
    extract_charges()
