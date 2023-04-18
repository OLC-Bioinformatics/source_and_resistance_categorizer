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

#sourcelist = ['Animal','Animal environment','Animal feces','Animal feed','Farm','Egg','Farm sewage','Fish/Seafood','Multi-product',
#              'Meat/Poultry','Reptile','Cider','Dairy','Food processing environment','Farm water','Flour','Fruit/Vegetables','Spice/Herbs','Insect','Nuts/Seeds',
#              'Plant','Sewage','Wastewater','Water','Tea']

#using a condensed sourcelist to keep things simpler
sourcelist = ['Egg','Fish/Seafood','Multi-product',
              'Meat/Poultry','Dairy','Food processing environment','Fruit/Vegetables']

#now do counts for gene combinations (args + biocide genes)
outfile ='{g}_AMR_plus_biocide_gene_counts.csv'.format(g=args.genus)

#will also use condensed ARG and biocide gene lists
#arglist = ["aac\(3\)","aac\(6'\)-Ib-cr","aadA","aph\(3''\)-Ib","aph\(3'\)","aph\(6\)-Id","blaACT","blaCARB","blaCMY",
#           "blaCMY-2","blaCTX-M","blaGES","blaIMP","blaKPC","blaNDM","blaOXA","blaPER","blaSHV","blaTEM","blaVIM",
#           "catA","cmlA","dfrA","mec","mcr-","mcr-1","mcr-9","qnrS","sul","tet","van","gyrA","parC","parE"]
arglist = ["aac\(3\)","aac\(6'\)-Ib-cr","aadA","aph\(3''\)-Ib","aph\(3'\)","aph\(6\)-Id","blaCMY",
           "blaCMY-2","blaCTX-M","blaIMP","blaKPC","blaNDM","blaOXA","blaPER","blaSHV","blaTEM","blaVIM",
           "catA","cmlA","dfrA","mec","mcr-","qnrS","sul","tet","van"]

biocidelist = ['qac',
               'bcrB','crcB', 'lmrS','smr', 'emrE'] #using bcrB for bcrABC

with open(outfile, 'w') as file:
    csv_file = csv.writer(file, delimiter=',')
    with open(outfile, 'a+') as file:
        file.write("Genus,total_genus,Source,Gene1,Gene2,total_source,amr_only,both_genes\n")
    for genus in generalist:
        print("Counting ARG presence for: ", genus)
        counttotal = inputdata.query('scientific_name.str.contains("{g}", na=False)'.format(g=genus))['scientific_name'].count()
        for source in sourcelist:
            countsource = inputdata.query('scientific_name.str.contains("{g}", na=False) & Source=="{s}"'.format(g=genus,s=source))['scientific_name'].count()
            for gene in arglist:
                countg = inputdata.query('scientific_name.str.contains("{g}", na=False) & Source=="{s}" & AMR_genotypes.str.contains("{arg}", na=False)'.format(g=genus,s=source, arg=gene))['scientific_name'].count()
                for bio in biocidelist:
                    countarg = inputdata.query('scientific_name.str.contains("{g}", na=False) & Source=="{s}" '
                                               '& AMR_genotypes.str.contains("{arg}", na=False) & stress_genotypes.str.contains("{brg}", na=False)'.format(g=genus,s=source,arg=gene,brg=bio))['scientific_name'].count()
                    with open(outfile, 'a+') as file:
                        file.write("{g},{cg},{s},{arg},{brg},{counts},{ao},{countarg}\n".format(g=genus,cg=counttotal,s=source,arg=gene,brg=bio,ao=countg,counts=countsource,countarg=countarg))

#add in the clinical data
clinicalsource = inputdata.query('scientific_name.str.contains("{g}", na=False) & epi_type=="clinical" & host=="Homo sapiens"'.format(g=genus))['scientific_name'].count()
for gene in arglist:
    countg = inputdata.query('scientific_name.str.contains("{g}", na=False) & epi_type=="clinical" & host=="Homo sapiens" & AMR_genotypes.str.contains("{arg}", na=False)'.format(g=genus,arg=gene))['scientific_name'].count()
    for bio in biocidelist:
        countcarg = inputdata.query('scientific_name.str.contains("{g}", na=False) & epi_type=="clinical" & host=="Homo sapiens" '
                                   '& AMR_genotypes.str.contains("{arg}", na=False) & stress_genotypes.str.contains("{brg}", na=False)'.format(g=genus,arg=gene,brg=bio))['scientific_name'].count()
        with open(outfile, 'a+') as file:
            file.write("{g},{cg},Clinical,{arg},{brg},{counts},{ao},{countarg}\n".format(g=genus,cg=counttotal,arg=gene,brg=bio,ao=countg,counts=clinicalsource,countarg=countcarg))

#fix the naming for genes that contain brackets
with open(outfile, 'r') as file:
    filedata = file.read()
filedata = filedata.replace("aac\(3\)","aac(3)")
filedata = filedata.replace("aac\(6'\)-Ib-cr","aac(6')-Ib-cr")
filedata = filedata.replace("aph\(3''\)-Ib","aph(3'')-Ib")
filedata = filedata.replace("aph\(3'\)","aph(3')")
filedata = filedata.replace("aph\(6\)-Id","aph(6)-Id")
#filedata = filedata.replace('qacE,','qacE')
filedata = filedata.replace('bcrB','bcrABC')
#rewrite the output after removal
with open(outfile, 'w') as file:
    file.write(filedata)



