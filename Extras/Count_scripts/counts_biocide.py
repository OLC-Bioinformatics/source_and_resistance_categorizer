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
#import findspark
#import pyspark
#from pyspark.sql import SparkSession
#spark = SparkSession.builder.master("local[1]").appName("SparkByExamples.com").getOrCreate()
#import spark.implicits._
#import org.apache.spark.sql.functions.col

#descriptions and argument assignment
parser = argparse.ArgumentParser(description='Counts abundance of resistance classes and genes for each isolation source '
                                            'after parsing (using the source_and_resistance.py script). '
                                            'Source database last updated: 2023-03-14')
parser = argparse.ArgumentParser(description='details',
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-g', dest='genus', type=str, required=True, help="""Name of genus/organism to count""")
parser.add_argument('--info', default=None,
                   help='''
                   Counts for NCBI PathogenFinder Datasheets
                   Please cite "Cooper et al., INSERT CITATION"

                   Input should be in csv format
                   ''')
parser.add_argument('-i', dest='infile', type=str, required=True, help="""Input Filename.csv""")
#parser.add_argument('-o', dest='outfile', type=str, default="counts_output.csv", help="""Output Filename.csv""")
argcomplete.autocomplete(parser)
args = parser.parse_args()

#read in the sources database file
inputdata = pandas.read_csv(args.infile)

#can I do a for loop with multiple genera?
#generalist = ['Shigella', 'Escherichia coli']
generalist = ['{}'.format(args.genus)]
#print(generalist)

sourcelist = ['Animal','Animal environment','Animal feces','Animal feed','Farm','Egg','Farm sewage','Fish/Seafood','Multi-product',
              'Meat/Poultry','Reptile','Cider','Dairy','Food processing environment','Farm water','Flour','Fruit/Vegetables','Spice/Herbs','Insect','Nuts/Seeds',
              'Plant','Sewage','Wastewater','Water','Tea']


#now create count files for biocide and metal genes
biocidefile = '{g}_biocide_gene_counts.csv'.format(g=args.genus)
biocidelist = ['qac','qacEdelta','qacC','qacE,','qacA','qacB','qacF','qacG','qacH','qacJ','qacK','qacL','qacM','sugE',
               'bcrB','crcB','srp','smd','sde', 'lmrS','smr','ssmE','tbtR','ttgR','ttgT','mtrF', 'emrE'] #using bcrB for bcrABC

for genus in generalist:
    clinicaltotal = inputdata.query('scientific_name.str.contains("{g}", na=False) & epi_type=="clinical" & host=="Homo sapiens"'.format(g=genus))['scientific_name'].count()
    clinicalsource = inputdata.query('scientific_name.str.contains("{g}", na=False) & epi_type=="clinical" & host=="Homo sapiens"'.format(g=genus))['scientific_name'].count()

with open(biocidefile, 'w') as file:
    csv_file = csv.writer(file, delimiter=',')
    with open(biocidefile, 'a+') as file:
        file.write("Genus,Source,Gene,number,total\n")
    for genus in generalist:
        print("Counting biocide resistance gene presence for: ", genus)
        counttotal = inputdata.query('scientific_name.str.contains("{g}", na=False)'.format(g=genus))['scientific_name'].count()
        for source in sourcelist:
            countsource = inputdata.query('scientific_name.str.contains("{g}", na=False) & Source=="{s}"'.format(g=genus,s=source))['scientific_name'].count()
            for gene in biocidelist:
                countbioc = inputdata.query('scientific_name.str.contains("{g}", na=False) & Source=="{s}" '
                                           '& stress_genotypes.str.contains("{arg}", na=False)'.format(g=genus,s=source,arg=gene))['scientific_name'].count()
                with open(biocidefile, 'a+') as file:
                    file.write("{g},{cg},{s},{arg},{counts},{countarg}\n".format(g=genus,cg=counttotal,s=source,arg=gene,counts=countsource,countarg=countbioc))
        for gene in biocidelist:
            countclbioc = inputdata.query('scientific_name.str.contains("{g}", na=False) & epi_type=="clinical" & host=="Homo sapiens" '
                                          '& stress_genotypes.str.contains("{arg}", na=False)'.format(g=genus,arg=gene))['scientific_name'].count()
            with open(biocidefile, 'a+') as file:
                file.write("{g},{cg},Clinical,{arg},{counts},{countarg}\n".format(g=genus,cg=counttotal, arg=gene, counts=clinicalsource,
                                                                             countarg=countclbioc))
#remove the extra comma from the qacE, category and change bcrB to bcrABC
with open(biocidefile, 'r') as file:
    filedata = file.read()
filedata = filedata.replace('qacE,','qacE')
filedata = filedata.replace('bcrB','bcrABC')
#rewrite the output after removal
with open(biocidefile, 'w') as file:
    file.write(filedata)

