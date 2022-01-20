# AA_frequencies_project
Project folder for the Final Project of Softwareentwicklung.
This Git repository contains a pipeline to perform plot and result table of Amino acid to structure percentage of given or randomly chosen PDB-Structures.

## Installation
git clone https://github.com/c-mayer/AA_frequencies_project

## Install environment
sudo install dssp

## Setup
You first have to give all files execute permission.
chmod +x ./bin/*
chmod +x ./01_download/01run.sh
chmod +x ./02_parse_pdb/01run.sh

## Use
cd 01_download
bash 01run.sh
cd ../02_parse_pdb
bash 01run.sh
cd results

## Additinal function
We additionally implemented a possibility, to get results of a manually given input file with protein structure names.
If both driver scripts are executed with **default** as argument, the given file with structure names will be performed instead of a random structure name sample.
If not executed with default, random structure names will be performed.
It is important, to execute **both or none of the two driver scripts with default**. Own structures have to be written into the *downloaded_default_pdb_files.txt* file.

## Usage example (for own structure list)
cd 01_download/doc
cat "OWN PDB STRUCTURE LIST" > downloaded_default_pdb_files.txt
cd ..
bash 01run.sh default
cd ../02_parse_pdb
bash 01run.sh default
cd results

## Authors

