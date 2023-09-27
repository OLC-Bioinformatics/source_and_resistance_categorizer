import shutil
import glob
import argparse
import argcomplete
import os

#make sure the input is a path
def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

#descriptions and argument assignment
parser = argparse.ArgumentParser(description='Counts abundance of resistance classes and genes for each isolation source '
                                            'after parsing (using the source_and_resistance.py script). '
                                            'Source database last updated: 2023-03-14')
parser = argparse.ArgumentParser(description='details',
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)
#parser.add_argument('-g', dest='genus', type=str, required=True, help="""Name of genus/organism to count""")
parser.add_argument('--info', default=None,
                   help='''
                   Counts for NCBI PathogenFinder Datasheets
                   Please cite "Cooper et al., INSERT CITATION"

                   Input should be in csv format
                   ''')
parser.add_argument('--path', dest='infolder', type=dir_path, required=True, help="""Input Folder""")
parser.add_argument('-o', dest='outputfile', type=str, default="combined_counts.csv", help="""Output Filename.csv""")
argcomplete.autocomplete(parser)
args = parser.parse_args()


#import csv files from input folder
path = r'{}'.format(args.infolder)
allFiles = glob.glob(path + "/*.csv")
allFiles.sort()  # glob lacks reliable ordering, so impose your own if output order matters
output = '{}'.format(args.outputfile)
with open(output, 'wb') as outfile:
    for i, fname in enumerate(allFiles):
        with open(fname, 'rb') as infile:
            if i != 0:
                infile.readline()  # Throw away header on all but first file
            # Block copy rest of file from input to output without parsing
            shutil.copyfileobj(infile, outfile)
            print(fname + " has been imported.")
