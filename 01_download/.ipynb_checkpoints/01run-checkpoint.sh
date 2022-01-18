#!/usr/bin/env bash

# Strict mode
# https://olivergondza.github.io/2019/10/01/bash-strict-mode.html
# https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -euo pipefail
trap 's=$?; echo >&2 "$0: Error on line "$LINENO": $BASH_COMMAND"; exit $s' ERR
#set -x  # print each command before executing it

### Variable section
N_ENTRIES=250 #!!!!!!!!!!!!!!!!!!!!!!! maybe give bash as executable and give n_numbers as argument in command line

### End variable section

# Setup
mkdir -p results
mkdir -p doc

# Select dataset 
if [ $* == "default" ]; then
    if [ -e doc/downloaded_default_pdb_files.txt ]; then # if file with <filename> does exist
        rm -f results/*ent
        ../bin/select_and_download_from_PDB.py -r
    fi
else
    if [ ! -e doc/downloaded_pdb_files.txt ]; then # if file with <filename> does not exist
        ../bin/select_and_download_from_PDB.py -n $N_ENTRIES
    fi
fi

# Cleanup
mv pdb/* results && rmdir pdb #!!!!!!!!!!!!!!!!!!! needs directories to not throw an error
rmdir obsolete
#gzip results/*ent  # pack files to save space
