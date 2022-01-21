# AA_frequencies_project
Project folder for the Final Project of Softwareentwicklung.<br>
This Git repository contains a pipeline to perform plot and result table of Amino acid to structure percentage of given or randomly chosen PDB-Structures.

## Installation
git clone https://github.com/c-mayer/AA_frequencies_project.git

## Install environment
sudo install dssp

## Setup
You first have to give all files execute permission.<br>
chmod +x ./bin/*<br>
chmod +x ./01_download/01run.sh<br>
chmod +x ./02_parse_pdb/01run.sh<br>

## Use
01_download/01run.sh:<br>
If no argument is given, 250 random PDB structures will be chosen for calculation. If an integer is given as first argument, the program creates the given number of random PDB structures.<br>

cd 01_download<br>
bash 01run.sh<br>
cd ../02_parse_pdb<br>
bash 01run.sh<br>
cd results<br>

## Additional function
We additionally implemented a possibility, to get results of a manually given input file with PDB structure names.<br>
If both driver scripts are executed with **default** as argument, the given file with PDB structures will be performed instead of a random PDB structure sample.<br>
If not executed with default, random PDB structures will be performed.<br>
It is important, to execute **both or none of the two driver scripts with default**. Own structures have to be written into the *downloaded_default_pdb_files.txt* file.<br>
If the present file *downloaded_default_pdb_files.txt* is not modified, it will reproduce the results that were given as an example.<br>

## Usage example (for own structure list)
cd 01_download/doc<br>
cat "OWN PDB STRUCTURE LIST" > downloaded_default_pdb_files.txt<br>
cd ..<br>
bash 01run.sh default<br>
cd ../02_parse_pdb<br>
bash 01run.sh default<br>
cd results<br>

## Authors
Dellinger Lorenz, Himmelbauer Florian, Mayer Christian
