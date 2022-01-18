#!/usr/bin/env python

import math
import argparse
from pathlib import Path
import numpy as np
import pandas as pd

# Column names
conf1 = "Helix"
conf2 = "Sheet"
conf3 = "Other"

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

# Possibly useful links
# https://www.shanelynn.ie/bar-plots-in-python-using-pandas-dataframes/
# https://www.python-graph-gallery.com/grouped-barplot
# https://stackoverflow.com/questions/24943991/change-grid-interval-and-specify-tick-labels-in-matplotlib

