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
parser = argparse.ArgumentParser(description='NCBI Source and Antibiotic Class Parser. '
                                            'Input and output should be in csv format. '
                                            'If using metadata files from NCBI PathogenFinder FTP, do not forget to remove the "#" in the first line. '
                                            'The "resistance_genes.csv" and "sources.csv" files must be in the same directory as this python script. '
                                            'Source database last updated: 2021-04-20')
parser = argparse.ArgumentParser(description='details',
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter)
#parser.add_argument('-db', dest='database_file', type=str, required=True, help="""source database file.csv""")
parser.add_argument('-g', dest='genus', type=str, required=True, help="""Name of genus to count""")
parser.add_argument('--info', default=None,
                   help='''
                   Count-IFs for NCBI PathogenFinder Datasheets
                   Please cite "Cooper et al., INSERT CITATION"

                   Input and output should be in csv format
                   ''')
parser.add_argument('-i', dest='infile', type=str, required=True, help="""Input Filename.csv""")
#parser.add_argument('-o', dest='outfile', type=str, default="counts_output.csv", help="""Output Filename.csv""")
argcomplete.autocomplete(parser)
args = parser.parse_args()

#read in the sources database file
inputdata = pandas.read_csv(args.infile)
#df
#inputdata = pandas.read_csv("counttest.csv")
#print(inputdata.head())

#find the count of ecoli
#ecoli_Count = inputdata.query('scientific_name=="Escherichia coli"')['scientific_name'].count()
#print("E.coli = ", ecoli_Count)

#shigella_Count = inputdata.query('scientific_name.str.contains("Shigella")')['scientific_name'].count()
#print("Shigella =", shigella_Count)

#find the count of ecoli from Meat/Poultry
#ecoli_meat = inputdata.query('scientific_name=="Escherichia coli" & Source=="Meat/Poultry"')['scientific_name'].count()
#print("Total E. coli = ",ecoli_Count, "Meat/Poultry", ecoli_meat)

#now add AMR
ecoli_meat_bla = inputdata.query('scientific_name.str.contains("Escherichia coli") & Source=="Meat/Poultry" & '\
'Antibiotic_Class.str.contains("betalactam")')['scientific_name'].count()
#print("with bla ", ecoli_meat_bla)

#can I do a for loop with multiple genera?
#generalist = ['Shigella', 'Escherichia coli']
generalist = ['{}'.format(args.genus)]
#print(generalist)

sourcelist = ['Animal','Animal environment','Animal feces','Animal feed','Farm','Egg','Farm sewage','Fish/Seafood','Multi-product',
              'Meat/Poultry','Reptile','Cider','Dairy','Food processing environment','Farm water','Flour','Fruit/Vegetables','Spice/Herbs','Insect','Nuts/Seeds',
              'Plant','Sewage','Wastewater','Water','Tea']

clsslist = ['aminoglycoside','betalactam','bleomycin','fosfomycin','fusidic acid','glycopeptide','MLS','macrolide',"lincosamide,",'lincosamide_streptogramin',
            'mupirocin','nitroimidazole','phenicol','phenicol_oxazolidinone','phenicol_quinolone','pluromutilin','polymyxin','quinolone','rifamycin',
            'streptogramin','streptothricin','sulphonamide','tetracenomycin','tetracycline','thiostrepton','trimethoprim','tuberactinomycin']

#tabfile = 'output_countif.csv
tabfile = '{g}_resistance_class_counts.csv'.format(g=args.genus)

with open(tabfile, 'w') as file:
    csv_file = csv.writer(file, delimiter=',') #could I avoid having to edit the lincosamide if I change this?
    with open(tabfile, 'a+') as file:
        file.write("Genus,Total_genus,Source,Class,total_from_source,number_res\n")
    for genus in generalist:
        print("Counting resistance classes for: ", genus)
        counttotal = inputdata.query('scientific_name.str.contains("{g}")'.format(g=genus))['scientific_name'].count()
        #print(genus, 'forlooptest', countf)
        for source in sourcelist:
            countsource = inputdata.query('scientific_name.str.contains("{g}") & Source=="{s}"'.format(g=genus,s=source))['scientific_name'].count()
            #print(genus,",",source,",", countr)
            for abxclss in clsslist:
                countc = inputdata.query('scientific_name.str.contains("{g}") & Source=="{s}" & Antibiotic_Class.str.contains("{c}")'.format(g=genus,s=source,c=abxclss))['scientific_name'].count()
                with open(tabfile, 'a+') as file:
                    file.write("{g},{t},{s},{c},{countt},{countc}\n".format(g=genus,t=counttotal,s=source,c=abxclss,countt=countsource,countc=countc))
            #add in biocide data
            countb = inputdata.query('scientific_name.str.contains("{g}") & Source=="{s}" & biocide.str.contains("biocide")'.format(g=genus,
                                                                                                                s=source))['scientific_name'].count()
            with open(tabfile, 'a+') as file:
                file.write("{g},{t},{s},Biocide,{countt},{countb}\n".format(g=genus,t=counttotal,s=source,countt=countsource,countb=countb))
            #add in metal data
            countm = inputdata.query('scientific_name.str.contains("{g}") & Source=="{s}" & Metal.str.contains("Metal")'.format(g=genus,
                                                                                                                s=source))['scientific_name'].count()
            with open(tabfile, 'a+') as file:
                file.write("{g},{t},{s},Metal,{countt},{countm}\n".format(g=genus,t=counttotal,s=source,countt=countsource,countm=countm))

#need to add data for the clinical source
clinicaltotal = inputdata.query('scientific_name.str.contains("{g}") & epi_type=="clinical" & host=="Homo sapiens"'.format(g=genus))['scientific_name'].count()
for abxclss in clsslist:
    clinicalbyclass = inputdata.query('scientific_name.str.contains("{g}") & epi_type=="clinical" & '
                                      'host=="Homo sapiens" & Antibiotic_Class.str.contains("{c}")'.format(g=genus,c=abxclss))['scientific_name'].count()
    with open(tabfile, 'a+') as file:
        file.write("{g},{t},Clinical,{c},{countt},{countc}\n".format(g=genus, t=counttotal, c=abxclss, countt=clinicaltotal,countc=clinicalbyclass))
# add in biocide data
countcb = inputdata.query('scientific_name.str.contains("{g}") & epi_type=="clinical" & host=="Homo sapiens"'
                         '& biocide.str.contains("biocide")'.format(g=genus))['scientific_name'].count()
with open(tabfile, 'a+') as file:
    file.write("{g},{t},Clinical,Biocide,{countt},{countb}\n".format(g=genus, t=counttotal, countt=clinicaltotal,
                                                                 countb=countcb))

# add in metal data
countcm = inputdata.query('scientific_name.str.contains("{g}") & epi_type=="clinical" & host=="Homo sapiens"'
                         '& Metal.str.contains("Metal")'.format(g=genus))['scientific_name'].count()
with open(tabfile, 'a+') as file:
    file.write("{g},{t},Clinical,Metal,{countt},{countm}\n".format(g=genus, t=counttotal, countt=clinicaltotal,
                                                                 countm=countcm))


#remove the extra comma from the lincosamide, category
#tabfile['Class'] = tabfile['Class'].str.replace('lincosamide,','lincosamide')
with open(tabfile, 'r') as file:
    filedata = file.read()
filedata = filedata.replace('lincosamide,','lincosamide')
#rewrite the output after removal
with open(tabfile, 'w') as file:
    file.write(filedata)


#now do counts for genes
argfile ='{g}_AMR_gene_counts.csv'.format(g=args.genus)

arglist = ["aac(3)","aac(6')-Ib-cr","aadA","aph(3'')-Ib","aph(3')","aph(6)-Id","blaACT","blaCARB","blaCMY",
           "blaCMY-2","blaCTX-M","blaGES","blaIMP","blaKPC","blaNDM","blaOXA","blaPER","blaSHV","blaTEM","blaVIM",
           "catA","cmlA","dfrA","mcr-","mcr-1","mcr-9","qnrS","sul","tet","van","gyrA","parC","parE"]

with open(argfile, 'w') as file:
    csv_file = csv.writer(file, delimiter=',')
    with open(argfile, 'a+') as file:
        file.write("Genus,Source,Gene,number,total\n")
    for genus in generalist:
        print("Counting ARG presence for: ", genus)
        for source in sourcelist:
            countsource = inputdata.query('scientific_name.str.contains("{g}") & Source=="{s}"'.format(g=genus,s=source))['scientific_name'].count()
            for gene in arglist:
                countarg = inputdata.query('scientific_name.str.contains("{g}") & Source=="{s}" '
                                           '& AMR_genotypes.str.contains("{arg}")'.format(g=genus,s=source,arg=gene))['scientific_name'].count()
                with open(argfile, 'a+') as file:
                    file.write("{g},{s},{arg},{counts},{countarg}\n".format(g=genus,s=source,arg=gene,counts=countsource,countarg=countarg))

#add in the clinical data
clinicalsource = inputdata.query('scientific_name.str.contains("{g}") & epi_type=="clinical" & host=="Homo sapiens"'.format(g=genus))['scientific_name'].count()
for gene in arglist:
    countcarg = inputdata.query('scientific_name.str.contains("{g}") & epi_type=="clinical" & host=="Homo sapiens" '
                               '& AMR_genotypes.str.contains("{arg}")'.format(g=genus,arg=gene))['scientific_name'].count()
    with open(argfile, 'a+') as file:
        file.write("{g},Clinical,{arg},{counts},{countarg}\n".format(g=genus,arg=gene,counts=clinicalsource,countarg=countcarg))


#now create count files for biocide and metal genes
biocidefile = '{g}_biocide_gene_counts.csv'.format(g=args.genus)
biocidelist = ['qac','qacEdelta','qacC','qacE,','qacA','qacB','qacF','qacG','qacH','qacJ','qacK','qacL','qacM','sugE',
               'bcrB','crcB','srp','smd','sde'] #using bcrB for bcrABC
with open(biocidefile, 'w') as file:
    csv_file = csv.writer(file, delimiter=',')
    with open(biocidefile, 'a+') as file:
        file.write("Genus,Source,Gene,number,total\n")
    for genus in generalist:
        print("Counting biocide resistance gene presence for: ", genus)
        for source in sourcelist:
            countsource = inputdata.query('scientific_name.str.contains("{g}") & Source=="{s}"'.format(g=genus,s=source))['scientific_name'].count()
            for gene in biocidelist:
                countbioc = inputdata.query('scientific_name.str.contains("{g}") & Source=="{s}" '
                                           '& stress_genotypes.str.contains("{arg}")'.format(g=genus,s=source,arg=gene))['scientific_name'].count()
                with open(biocidefile, 'a+') as file:
                    file.write("{g},{s},{arg},{counts},{countarg}\n".format(g=genus,s=source,arg=gene,counts=countsource,countarg=countbioc))
        for gene in biocidelist:
            countclbioc = inputdata.query('scientific_name.str.contains("{g}") & epi_type=="clinical" & host=="Homo sapiens" '
                                          '& stress_genotypes.str.contains("{arg}")'.format(g=genus,arg=gene))['scientific_name'].count()
            with open(biocidefile, 'a+') as file:
                file.write("{g},Clinical,{arg},{counts},{countarg}\n".format(g=genus, arg=gene, counts=clinicalsource,
                                                                             countarg=countclbioc))
#remove the extra comma from the qacE, category
with open(biocidefile, 'r') as file:
    filedata = file.read()
filedata = filedata.replace('qacE,','qacE')
filedata = filedata.replace('bcrB','bcrABC')
#rewrite the output after removal
with open(biocidefile, 'w') as file:
    file.write(filedata)

metalfile = '{g}_metal_gene_counts.csv'.format(g=args.genus)
metallist = ['ars','cad','chr','cnr','cop','cue','dps','fie','gol','kla','mco','mer','ncc','ncr','nir','nre','pco','sil',
             'tcr','ter']

with open(metalfile, 'w') as file:
    csv_file = csv.writer(file, delimiter=',')
    with open(metalfile, 'a+') as file:
        file.write("Genus,Source,Gene,number,total\n")
    for genus in generalist:
        print("Counting metal resistance gene presence for: ", genus)
        for source in sourcelist:
            countsource = inputdata.query('scientific_name.str.contains("{g}") & Source=="{s}"'.format(g=genus,s=source))['scientific_name'].count()
            for gene in metallist:
                countbioc = inputdata.query('scientific_name.str.contains("{g}") & Source=="{s}" '
                                           '& stress_genotypes.str.contains("{arg}")'.format(g=genus,s=source,arg=gene))['scientific_name'].count()
                with open(metalfile, 'a+') as file:
                    file.write("{g},{s},{arg},{counts},{countarg}\n".format(g=genus,s=source,arg=gene,counts=countsource,countarg=countbioc))
        for gene in metallist:
            countclbioc = inputdata.query('scientific_name.str.contains("{g}") & epi_type=="clinical" & host=="Homo sapiens" '
                                          '& stress_genotypes.str.contains("{arg}")'.format(g=genus,arg=gene))['scientific_name'].count()
            with open(metalfile, 'a+') as file:
                file.write("{g},Clinical,{arg},{counts},{countarg}\n".format(g=genus, arg=gene, counts=clinicalsource,
                                                                             countarg=countclbioc))