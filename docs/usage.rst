=====
Usage
=====

Importing promoe into your own project:
---------------------------------------
::

    import promoe

promoe's commandline interface:
-------------------------------

Promoe offers three not necessarily distinct entry points::

                 ____  ____   ___  __  __  ___  _____
                |  _ \|  _ \ / _ \|  \/  |/ _ \| ____|
                | |_) | |_) | | | | |\/| | | | |  _|
                |  __/|  _ <| |_| | |  | | |_| | |___
                |_|   |_| \_ \___/|_|  |_|\___/|_____|

Usage: promoe [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose  Verbose output (print debug statements)
  --help         Show this message and exit.

| Commands:
|   protonize
|   protonize-selected
|   clean-hydrogens

The help menus of the respective commands can be requested via::

    promoe <command> --help
    e.g. promoe protonize --help

promoe protonize
----------------

asd
