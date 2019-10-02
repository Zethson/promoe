#!/bin/bash

PROTONATE_SCRIPT_LOCATION=$1
PDB_ID=$2
moebatch -exec "script ['$PROTONATE_SCRIPT_LOCATION', '$PDB_ID']"
