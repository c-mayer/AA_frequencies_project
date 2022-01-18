#!/usr/bin/env bash

# Strict mode
# https://olivergondza.github.io/2019/10/01/bash-strict-mode.html
# https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -euo pipefail
trap 's=$?; echo >&2 "$0: Error on line "$LINENO": $BASH_COMMAND"; exit $s' ERR
#set -x  # print each command before executing it

### Variable section
N_ENTRIES=250

### End variable section

# Setup
mkdir -p results

# Select dataset 
if [ ! -e doc/downloaded_pdb_files.txt ]; then
  ../bin/select_and_download_from_PDB.py $N_ENTRIES
fi

# Cleanup
mv pdb/* results && rmdir pdb
rmdir obsolete
#gzip results/*ent  # pack files to save space
