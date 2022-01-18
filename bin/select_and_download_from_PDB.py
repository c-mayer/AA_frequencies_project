#!/usr/bin/env python

"""Get PDB index, randomly select a number of entries, and download them.

More info:
- https://biopython.org/wiki/The_Biopython_Structural_Bioinformatics_FAQ
- https://github.com/biopython/biopython/blob/master/Bio/PDB/PDBList.py
- http://biopython.org/DIST/docs/tutorial/Tutorial.html#sec242
"""

import sys
import os
import random
import logging
import argparse
from Bio.PDB import PDBList

# Create logger
# https://www.youtube.com/watch?v=jxmzY9soFXg
# https://realpython.com/python-logging/
# https://stackoverflow.com/a/56144390/
# https://docs.python.org/3/howto/logging.html#changing-the-format-of-displayed-messages
logging.basicConfig(
    level=logging.NOTSET, format=" %(levelname)-7s:: %(message)s"
)  # configure root logger
logger = logging.getLogger(__name__)  # create custom logger
logger.setLevel(logging.DEBUG)  # set level for custom logger


def get_index_file():
    """Get PDB index file. Return a list of PDB codes in the index file."""
    # https://github.com/biopython/biopython/blob/master/Bio/PDB/PDBList.py
    pdbl = PDBList()
    all_entries = pdbl.get_all_entries()
    logger.info(f"Downloaded PDB index file with {len(all_entries)} entries.")
    return all_entries


def select_random_subset(all_entries, n_entries):
    """Select random subset of entries."""
    selected = random.sample(all_entries, n_entries * 2)
    # The motivation to select more entries than required is that
    # some files can't be downloaded ("Desired structure doesn't exist"),
    # so we may need additional entries
    logger.info(f"Randomly selected {n_entries} entries from {len(all_entries)} entries.")
    return selected


def download_pdb_files(selected_entries, n_entries):
    """Download pdb files by entry name."""
    pdbl = PDBList()
    n_downloaded = 0
    while n_downloaded < n_entries:
        entry = selected_entries.pop()
        # https://biopython.org/docs/latest/api/Bio.PDB.PDBList.html#Bio.PDB.PDBList.PDBList.retrieve_pdb_file
        outfile = pdbl.retrieve_pdb_file(entry.strip(), file_format="pdb", pdir="pdb")
        # Some structures may not exist ("Desired structure doesn't exist")
        if os.path.exists(outfile):
            with open("downloaded_pdb_files.txt", "a") as f:
                print(entry, file=f)  # structure exists -> write to logfile
            n_downloaded += 1
    logger.info(f"Downloaded {n_downloaded} pdb files. Entry names saved in 'downloaded_pdb_files.txt'.")


def main(n_entries):
    all_entries = get_index_file()
    selected_entries = select_random_subset(all_entries, n_entries)
    download_pdb_files(selected_entries, n_entries)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Randomly select and download a number of PDB entries."
    )
    parser.add_argument("n_entries", type=int, metavar="N", help="Number of entries")
    args = parser.parse_args()

    main(args.n_entries)
