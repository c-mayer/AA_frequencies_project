#!/usr/bin/bash env
set -euo pipefail
trap 's=$?; echo >&2 "$0: Error on line "$LINENO": $BASH_COMMAND"; exit $s' ERR

### prove input given
if [[ "$#" -gt 1 ]]; then
    echo 'Illegal number of parameters. Please use only one argument ("default" for working with own structure names or no argument for random PDB structures).'
    exit
fi

### Setup
mkdir -p data results tmp doc
rm -rf data/* results/* tmp/*

cd data
# In case we have packed files
#for F in ../../01_*/results/*gz; do
#  ln -s $F
#done
# Unpack files
#for F in ./*gz; do
#  gunzip -c $F > ../tmp/${F%%.gz}
#done
for F in ../../01_*/results/*ent; do
  ln -s $F
done

# rename symbolic links from .ent to .pdb for further parsing
for F in *.ent; do
  mv "$F" "${F/.ent/.pdb}"
done

cd ../doc

# symbolic link for pdb structure names
if [[ $* == "default" ]]; then
  rm -f downloaded_pdb_files.txt
  ln -s ../../01_*/doc/downloaded_default_pdb_files.txt
  mv downloaded_default_pdb_files.txt downloaded_pdb_files.txt
else
  rm -f downloaded_pdb_files.txt
  ln -s ../../01_*/doc/downloaded_pdb_files.txt
fi

cd ..

### Perform workflow
# Parse files and write AA frequency tables
../bin/parse_pdb_files.py data 2> doc/parse_pdb_files.log
mv *tsv results

# Visualize AA frequency tables
for F in results/*tsv; do
  ../bin/plot_multibar.py $F
done


### Cleanup
rm -rf tmp
