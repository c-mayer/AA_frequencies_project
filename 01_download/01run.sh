#!/usr/bin/env bash

# Strict mode
# https://olivergondza.github.io/2019/10/01/bash-strict-mode.html
# https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -euo pipefail
trap 's=$?; echo >&2 "$0: Error on line "$LINENO": $BASH_COMMAND"; exit $s' ERR
#set -x  # print each command before executing it

### prove input given
if [[ "$#" -gt 1 ]]; then
    echo 'Illegal number of parameters. Please use only one argument ("default" for working with own structure names or integer for number of random PDB structures chosen).
If no argument is given, 250 random PDB structures will be chosen.'
    exit
fi

### Variable section
N_ENTRIES=250

if [[ $* =~ ^[0-9]+$ ]]; then
	N_ENTRIES=$1 # gives number of entries as input
fi
### End variable section


# Setup
mkdir -p results
mkdir -p doc

# Select dataset 
if [[ $* == "default" ]]; then
    if [ -e doc/downloaded_default_pdb_files.txt ]; then # if file with <filename> does exist
        rm -f results/*ent
        ../bin/select_and_download_from_PDB.py -r
    fi
else
    if [ ! -e doc/downloaded_pdb_files.txt ]; then # if file with <filename> does not exist
        ../bin/select_and_download_from_PDB.py -n $N_ENTRIES
        mv downloaded_pdb_files.txt -t doc
    fi
fi

# Cleanup
mv pdb/* results && rmdir pdb
rmdir obsolete
#gzip results/*ent  # pack files to save space
