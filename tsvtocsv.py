#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

import csv
import os.path

import pandas
import argparse
import argcomplete
import regex as re
import numpy as np
from regex import search

parser = argparse.ArgumentParser(description='details',
         usage='use "%(prog)s --help" for more information',
         formatter_class=argparse.RawTextHelpFormatter)
#parser.add_argument('-db', dest='database_file', type=str, required=True, help="""source database file.csv""")
parser.add_argument('--info', default=None,
                    help='''

                    ''')
parser.add_argument('-i', dest='infile', type=str, required=True, help="""Input Filename.csv""")
#parser.add_argument('-o', dest='outfile', type=str, default="out_source_parser", help="""Output Filename.csv""")
argcomplete.autocomplete(parser)
args = parser.parse_args()

tsv_file = args.infile

#read tsv file
csv_table = pandas.read_table(tsv_file, sep='\t')

#convert to csv
fbasename = os.path.split(tsv_file)[1].split('.')[0]
fname = os.path.join(fbasename + '.csv')
csv_table.to_csv(fname, index=False)

