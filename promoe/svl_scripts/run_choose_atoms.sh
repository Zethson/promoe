#!/bin/bash
CHOOSE_ATOMS_SCRIPT_LOCATION=$1
PDB_ID=$2
# shellcheck disable=SC2124
ATOMS="${@:3}"

moebatch -exec "script ['$CHOOSE_ATOMS_SCRIPT_LOCATION', ['$PDB_ID', $ATOMS]]"
