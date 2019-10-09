import logging

from sys import argv
from pymol import cmd
import psico.fullinit

console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
LOG = logging.getLogger("Extract Distances")
LOG.addHandler(console)
LOG.setLevel(logging.INFO)

pdb_file = argv[1]
distance = argv[2]
if not 'binding_site' in pdb_file:
    LOG.warn('Trying to extract distances from non binding_site pdb file. May cause issues downstream!')

if not 'protonated' in pdb_file:
    LOG.warn('Trying to extract distances from a possibly non protonated pdb file.'
             'This is not intended and you likely will not receive any distances. The reason is that there likely '
             'won\' be any hydrogens.')

LOG.info('Extracting distances for %s' % pdb_file)

cmd.reinitialize()
cmd.load(pdb_file)

ligand = cmd.select("ligand", "organic")
hydrogens = cmd.select("hydrogen", "name h")
distance = cmd.distance("hbonds", "ligand", "hydrogen", distance, mode=0)
raw_distances = cmd.get_raw_distances("hbonds")

file_name = pdb_file.split('/')[-1].replace('.pdb_protonated.mol2', '')
with open(file_name + '_distances', 'w') as f:
    for distance in raw_distances:
        f.write(str(distance) + '\n')
