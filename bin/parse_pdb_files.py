#!/usr/bin/env python

"""Parse pdb files and determine for each amino acid how often
it participates in different secondary structures. Write results
as tsv file."""

import logging
import argparse
#from collections import Counter, OrderedDict
from pathlib import Path
from Bio.PDB import PDBParser, DSSP
from Bio import Data
import pandas as pd
import numpy as np

# Create logger
logging.basicConfig(
    level=logging.NOTSET, format=" %(levelname)-7s:: %(message)s"
)  # configure root logger
logger = logging.getLogger(__name__)  # create custom logger
logger.setLevel(logging.DEBUG)  # set level for custom logger

protein_letters = Data.CodonTable.IUPACData.protein_letters


def create_pdb_list():
    """Get list of pdb structure names."""
    pdb_list = []
    with open("./doc/downloaded_pdb_files.txt", "r") as f:
        for line in f:
            l = line.strip()
            l = l.lower()
            pdb_list.append(l)
    f.close()
    return pdb_list

def parse_all_structure_files(pdb_list, pdb_dir):
    """Parses relevant information of all structures and saves it in a tuple list."""
    # create dict for grouping in three main structures
    structure_dict = {'H':'Helix','G':'Helix','I':'Helix','B':'Sheet','E':'Sheet','T':'Other','S':'Other','-':'Other'}
    # create storage for tuples
    tuple_list = []
    # parse data from strucutre files
    p = PDBParser()
    for pdb in pdb_list:
        structure = p.get_structure(pdb, f'./{pdb_dir}/pdb{pdb}.pdb')
        # use only the first model
        model = structure[0]
        # calculate DSSP
        dssp = DSSP(model, f'./{pdb_dir}/pdb{pdb}.pdb')
        # parse tuples from DSSP object
        for i in range (len(dssp)):
            a_key = dssp[dssp.keys()[i]]
            tup = (a_key[1], structure_dict[a_key[2]])
            tuple_list.append(tup)
    return tuple_list

def count_AA_structure_pairs(tuple_list):
    """Loops (AminoAcid, strucuture) tuples and counts it to matrix."""
    # create numpy array with zeros
    count_table = np.zeros(shape=(20,3))
    count_table
    # dicts to convert AA and structure to numpy coordinates
    AA_pos_dict = {'A': 0,'C': 1,'D': 2,'E': 3,'F': 4,'G': 5,'H': 6,'I': 7,'K': 8,'L': 9,'M': 10,'N': 11,'P': 12,'Q': 13,'R': 14,'S': 15,'T': 16,'V': 17,'W': 18,'Y': 19}
    struct_pos_dict = {'Helix': 0, 'Sheet': 1, 'Other': 2}
    # adds counting to matrix
    for i, j in tuple_list: # i is AA, j is structure
        count_table[AA_pos_dict[i], struct_pos_dict[j]] += 1
    return count_table

def calc_count_table(count_table):
    """Takes a count_table as input and calculates percentage for each entry like (value/total_value)*100.
    Rounds result to 2 decimals."""
    # calculate sum of count_table
    sum_AA = np.sum(count_table)
    # calculate percentage from count
    freq_table = (count_table / sum_AA) * 100
    freq_table = np.round(freq_table, decimals=2)
    return freq_table

def add_AA_to_table(freq_table):
    """Creates AA numpy array and adds it to the input table."""
    # create column for AA's
    AA_list = np.array([['A'], ['C'], ['D'], ['E'], ['F'], ['G'], ['H'], ['I'], ['K'], ['L'], ['M'], ['N'], ['P'], ['Q'], ['R'], ['S'], ['T'], ['V'], ['W'], ['Y']])
    # append column to numpy array
    AA_freq_table = np.append(AA_list, freq_table, axis=1)
    return AA_freq_table

def create_dataframe(AA_freq_table):
    """Takes numpy array with added AA's and converts it to pandasDataFrame with headers."""
    # create pandasDataframe from numpy array
    df_freq_table = pd.DataFrame(AA_freq_table, columns=['AA', 'Helix', 'Sheet', 'Other'])
    return df_freq_table


def main(pdb_dir):
    logger.info(f"Directory with PDB files: {pdb_dir}")
    pdb_list = create_pdb_list()
    tuple_list = parse_all_structure_files(pdb_list, pdb_dir)
    count_table = count_AA_structure_pairs(tuple_list)
    freq_table = calc_count_table(count_table)
    AA_freq_table = add_AA_to_table(freq_table)
    df_freq_table = create_dataframe(AA_freq_table)
    df_freq_table.to_csv("./AA_freq_table.tsv", sep="\t", index=False)

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

