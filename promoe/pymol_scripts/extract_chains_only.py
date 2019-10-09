import logging

from pymol import cmd
from sys import argv

console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
LOG = logging.getLogger("Extract Chains")
LOG.addHandler(console)
LOG.setLevel(logging.INFO)

# This script extracts the selected chain only and saves it as a pdb.

all_argv = argv[1:]
pdb_id = all_argv[0]
chain = all_argv[1]

cmd.reinitialize()
cmd.load(pdb_id)

cmd.select("chain", "chain %s" % chain)

cmd.save("%s_chain_%s.pdb" % (pdb_id.split('/')[-1][:-4], chain), "chain")
