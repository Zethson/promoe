# -*- coding: utf-8 -*-

"""Console script for promoe."""
import logging
import os
import sys
import click

from promoe.util.command_util import is_tool_accessible

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
    type=click.Path(exists=True),
    nargs=-1,
    required=True,
)
def protonize(pdbs):
    LOG.info('Protonize')


def main(args=None):
    """Console script for promoe."""

    print('''                 ____  ____   ___  __  __  ___  _____
                |  _ \|  _ \ / _ \|  \/  |/ _ \| ____|
                | |_) | |_) | | | | |\/| | | | |  _|
                |  __/|  _ <| |_| | |  | | |_| | |___
                |_|   |_| \_ \\___/|_|  |_|\___/|_____|''')

    # with open(WD + '/svl_scripts/test_svl.txt', 'r') as f: content = f.readlines()
    # print(content)

    print(is_tool_accessible('moebatch'))
    print(is_tool_accessible('pymol'))
    print(is_tool_accessible('hxfghfgh'))

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
