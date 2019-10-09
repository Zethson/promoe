import logging

from pymol import cmd
from sys import argv
import sys
from collections import defaultdict

console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
LOG = logging.getLogger("Extract Ligands")
LOG.addHandler(console)
LOG.setLevel(logging.INFO)

all_argv = argv[1:]

"""
Script which uses pymol to extract all ligands and their respective IDs.
"""

for pdb_id in all_argv:
    cmd.reinitialize()
    cmd.fetch(pdb_id)

    cmd.save("%s_full.pdb" % pdb_id, "all")

    cmd.select("ligand", "organic")
    cmd.remove("resn HOH or resn Zn")

    # temporarily redirect stdout to get all ligand IDs
    sys.stdout = open('%s_ligand_ids' % pdb_id, 'w')
    cmd.iterate("bymol het", "print resi, resn, ID, chain")

    # reset cmd, since we want the HOH back
    cmd.reinitialize()
    cmd.fetch(pdb_id)

    # restore stdout
    sys.stdout = sys.__stdout__

    # fetch all ligand IDs and their chains
    resn_to_chains = defaultdict(set)
    with open("%s_ligand_ids" % pdb_id, 'r') as f:
        for line in f.readlines():
            content = str.split(line)
            resn_to_chains[content[1]] |= {content[3]}

    # save ligand + binding site
    for resn in resn_to_chains.keys():
        for chain in resn_to_chains[resn]:
            cmd.select("ligand_only", "organic and resn %s and chain %s" % (resn, chain))

            cmd.select("binding_site", "organic and resn %s and chain %s" % (resn, chain))
            cmd.select("binding_site", "binding_site expand 5.0 extend 2")
            cmd.select("binding_site", "br. binding_site")

            cmd.save("%s_%s_chain_%s_binding_site.pdb" % (pdb_id, resn, chain), "binding_site")
            cmd.save("%s_%s_chain_%s_ligand_only.pdb" % (pdb_id, resn, chain), "ligand_only")
