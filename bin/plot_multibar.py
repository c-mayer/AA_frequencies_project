#!/usr/bin/env python

import math
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Parse arguments
parser = argparse.ArgumentParser(
    description="""FILE is a file with rows and columns 'Helix', 'Sheet',
    'Other' in tab-separated format. The script plots the rows as distinct
    labels on the x-axis, and the columns as multibars."""
)
parser.add_argument("infile", metavar="FILE", help="Input file")
args = parser.parse_args()

# Read file
df = pd.read_csv(args.infile, sep="\t")

# Generate plot for AA
fig = df.set_index('AA').plot.bar()
plt.title("Amino acid Frequencies in secondary Structure")
plt.xlabel("Amino Acid")
plt.ylabel("Realtive frequency (%)")
plt.grid(axis="y", alpha=0.5)
plt.savefig("./results/AA_frequency_plot.pdf", dpi=100)
plt.close()

