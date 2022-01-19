#!/usr/bin/env python

"""Parse pdb files and determine for each amino acid how often
it participates in different secondary structures. Write results
as tsv file.

PDB file format: https://www.wwpdb.org/documentation/file-format-content/format33/sect1.html

A PDB file consists of multiple sections: Title, Primary structure, Heterogen
section, Secondary structure, Connectivity annotation, etc.

Primary structure section
https://www.wwpdb.org/documentation/file-format-content/format33/sect3.html
Contains the sequence of residues in each chain of the macromolecule.

Secondary structure section
https://www.wwpdb.org/documentation/file-format-content/format33/sect5.html
Describes helices, sheets, and turns found in protein and polypeptide
structures. There are three possible records: HELIX, TURN and SHEET

One possibility is to write a parser for PDB files that extracts the
information from the "secondary structure section". Alternatively,
we can use tools like DSSP or other secondary structure prediction tools
to determine the sec. structure from atomic positions. Some possibly
relevant links:
- https://www.biostars.org/p/48/
- https://www.biostars.org/p/65055/
- https://www.researchgate.net/post/Is_there_a_way_to_search_the_PDB_for_secondary_structure_followed_by_a_sequence_motif
- https://en.wikipedia.org/wiki/Protein_secondary_structure
- https://en.wikipedia.org/wiki/DSSP_(hydrogen_bond_estimation_algorithm)

Biopython PDB package:
- https://biopython.org/docs/latest/api/Bio.PDB.html
- https://github.com/biopython/biopython/tree/master/Bio/PDB
- https://biopython.org/wiki/The_Biopython_Structural_Bioinformatics_FAQ
- http://biopython.org/DIST/docs/tutorial/Tutorial.html#sec182

The Biopython tutorial suggests to use DSSP to obtain secondary structure info, so
that seems like a reasonable choice.
"""

import logging
import argparse
from collections import Counter, OrderedDict
from pathlib import Path
from Bio.PDB import PDBParser, DSSP
from Bio import Data

# Create logger
logging.basicConfig(
    level=logging.NOTSET, format=" %(levelname)-7s:: %(message)s"
)  # configure root logger
logger = logging.getLogger(__name__)  # create custom logger
logger.setLevel(logging.DEBUG)  # set level for custom logger


# https://biopython.org/wiki/The_Biopython_Structural_Bioinformatics_FAQ
# "How do I determine secondary structure?" -> DSSP codes
DSSP_codes = dict(
    [
        ("Helix", "H"),
        ("Bridge", "B"),
        ("Strand", "E"),
        ("3-10 Helix", "G"),
        ("Pi-Helix", "I"),
        ("Turn", "T"),
        ("Bend", "S"),
        ("Other", "-"),
    ]
)

protein_letters = Data.CodonTable.IUPACData.protein_letters


pdb_list = ['131l']

p = PDBParser()
for i in pdb_list:
    structure = p.get_structure(i, 'pdb%s.ent' % i)
    # use only the first model
    model = structure[0]
    # calculate DSSP
    dssp = DSSP(model, './pdb%s.ent' % i)
    # extract sequence and secondary structure from the DSSP tuple
    sequence = ''
    sec_structure = ''
    for z in range(len(dssp)):
        a_key = list(dssp.keys())[z]
        sequence += dssp[a_key][1]
        sec_structure += dssp[a_key][2]

    # print extracted sequence and structure
    print(i)
    print(sequence)
    #print(sec_structure)
    sec_structure = sec_structure.replace('-', 'O')
    sec_structure = sec_structure.replace('I', 'H')
    sec_structure = sec_structure.replace('T', 'O')
    sec_structure = sec_structure.replace('S', 'O')
    sec_structure = sec_structure.replace('G', 'H')
    sec_structure = sec_structure.replace('B', 'S')
    sec_structure = sec_structure.replace('E', 'S')
    print(sec_structure)


# Parsed DSSP file to  dataframe
parser = parseDSSP('131l.dssp')
parser.parse()
pddict = parser.dictTodataframe()

def main(pdb_dir):
    logger.info(f"Directory with PDB files: {pdb_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""The script outputs a table of AA frequencies in
        different secondary structures, as determined by the DSSP algorithm,
        https://en.wikipedia.org/wiki/DSSP_(hydrogen_bond_estimation_algorithm)."""
    )
    parser.add_argument(
        "pdb_dir", metavar="DIR", help="Directory with files in pdb format"
    )
    args = parser.parse_args()

    main(args.pdb_dir)
