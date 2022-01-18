#!/usr/bin/bash env
set -euo pipefail
trap 's=$?; echo >&2 "$0: Error on line "$LINENO": $BASH_COMMAND"; exit $s' ERR

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

