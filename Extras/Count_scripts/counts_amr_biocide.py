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

sourcelist = ['Animal','Animal environment','Animal feces','Animal feed','Raw pet food','Pet food','Farm','Egg','Farm sewage','Fish/Seafood','Multi-product',
              'Meat/Poultry','Reptile','Cider','Dairy','Food processing environment','Farm water','Flour','Fruit/Vegetables','Spice/Herbs','Insect','Nuts/Seeds',
              'Plant','Sewage','Wastewater','Water','Tea']

clsslist = ['aminoglycoside','betalactam','bleomycin','fosfomycin','fusidic acid','glycopeptide','MLS','macrolide',"lincosamide,",'lincosamide_streptogramin',
            'mupirocin','nitroimidazole','phenicol','phenicol_oxazolidinone','phenicol_quinolone','pluromutilin','polymyxin','quinolone','rifamycin',
            'streptogramin','streptothricin','sulphonamide','tetracenomycin','tetracycline','thiostrepton','trimethoprim','tuberactinomycin']

#tabfile = 'output_countif.csv
tabfile = '{g}_resistance_plus_biocide_counts.csv'.format(g=args.genus)

with open(tabfile, 'w') as file:
    csv_file = csv.writer(file, delimiter=',') #could I avoid having to edit the lincosamide if I change this?... no
    with open(tabfile, 'a+') as file:
        file.write("Genus,Total_genus,Source,Class,compare,total_from_source,number_res\n")
    for genus in generalist:
        print("Counting resistance classes for: ", genus)
        counttotal = inputdata.query('scientific_name.str.contains("{g}", na=False)'.format(g=genus))['scientific_name'].count()
        #print(genus, 'forlooptest', countf)
        for source in sourcelist:
            countsource = inputdata.query('scientific_name.str.contains("{g}", na=False) & Source=="{s}"'.format(g=genus,s=source))['scientific_name'].count()
            #print(genus,",",source,",", countr)
            for abxclss in clsslist:
                countc = inputdata.query('scientific_name.str.contains("{g}", na=False) & Source=="{s}" & Antibiotic_Class.str.contains("{c}", na=False) & biocide.str.contains("biocide", na=False)'.format(g=genus,s=source,c=abxclss))['scientific_name'].count()
                with open(tabfile, 'a+') as file:
                    file.write("{g},{t},{s},{c},Biocide,{countt},{countc}\n".format(g=genus,t=counttotal,s=source,c=abxclss,countt=countsource,countc=countc))
            #add in biocide data
            #countb = inputdata.query('scientific_name.str.contains("{g}", na=False) & Source=="{s}" & biocide.str.contains("biocide", na=False)'.format(g=genus,
            #                                                                                                    s=source))['scientific_name'].count()
            #with open(tabfile, 'a+') as file:
            #    file.write("{g},{t},{s},Biocide,{countt},{countb}\n".format(g=genus,t=counttotal,s=source,countt=countsource,countb=countb))
            #add in metal data
            countm = inputdata.query('scientific_name.str.contains("{g}", na=False) & Source=="{s}" & Metal.str.contains("Metal", na=False) & biocide.str.contains("biocide", na=False)'.format(g=genus,
                                                                                                                s=source))['scientific_name'].count()
            with open(tabfile, 'a+') as file:
                file.write("{g},{t},{s},Metal,Biocide,{countt},{countm}\n".format(g=genus,t=counttotal,s=source,countt=countsource,countm=countm))

#need to add data for the clinical source
clinicaltotal = inputdata.query('scientific_name.str.contains("{g}", na=False) & epi_type=="clinical" & host=="Homo sapiens"'.format(g=genus))['scientific_name'].count()
for abxclss in clsslist:
    clinicalbyclass = inputdata.query('scientific_name.str.contains("{g}", na=False) & epi_type=="clinical" & '
                                      'host=="Homo sapiens" & Antibiotic_Class.str.contains("{c}", na=False) & biocide.str.contains("biocide", na=False)'.format(g=genus,c=abxclss))['scientific_name'].count()
    with open(tabfile, 'a+') as file:
        file.write("{g},{t},Clinical,{c},Biocide,{countt},{countc}\n".format(g=genus, t=counttotal, c=abxclss, countt=clinicaltotal,countc=clinicalbyclass))
# add in biocide data
#countcb = inputdata.query('scientific_name.str.contains("{g}", na=False) & epi_type=="clinical" & host=="Homo sapiens"'
#                         '& biocide.str.contains("biocide", na=False)'.format(g=genus))['scientific_name'].count()
#with open(tabfile, 'a+') as file:
#    file.write("{g},{t},Clinical,Biocide,{countt},{countb}\n".format(g=genus, t=counttotal, countt=clinicaltotal,
#                                                                 countb=countcb))

# add in metal data
countcm = inputdata.query('scientific_name.str.contains("{g}", na=False) & epi_type=="clinical" & host=="Homo sapiens"'
                         '& Metal.str.contains("Metal", na=False) & biocide.str.contains("biocide", na=False)'.format(g=genus))['scientific_name'].count()
with open(tabfile, 'a+') as file:
    file.write("{g},{t},Clinical,Metal,Biocide,{countt},{countm}\n".format(g=genus, t=counttotal, countt=clinicaltotal,
                                                                 countm=countcm))


#remove the extra comma from the lincosamide, category
#tabfile['Class'] = tabfile['Class'].str.replace('lincosamide,','lincosamide')
with open(tabfile, 'r') as file:
    filedata = file.read()
filedata = filedata.replace('lincosamide,','lincosamide')
#rewrite the output after removal
with open(tabfile, 'w') as file:
    file.write(filedata)


