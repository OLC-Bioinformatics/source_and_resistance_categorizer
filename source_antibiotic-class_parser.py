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

#descriptions and argument assignment
parser = argparse.ArgumentParser(description='NCBI Source and Antibiotic Class Parser. '
                                             'Input and output should be in csv format. '
                                             'If using metadata files from NCBI PathogenFinder FTP, do not forget to remove the "#" in the first line. '
                                             'The "amrgenes.csv" file should be in the same directory as this script. '
                                             'Source database last updated: 2021-04-20')
parser.add_argument('-db', dest='database_file', type=str, required=True, help="""source database file.csv""")
parser.add_argument('-i', dest='infile', type=str, required=True, help="""Input Filename.csv""")
parser.add_argument('-o', dest='outfile', type=str, default="out_source_parser", help="""Output Filename.csv""")
argcomplete.autocomplete(parser)
args = parser.parse_args()

#read in the sources database file
data = pandas.read_csv(args.database_file)

#use the column headers in the source database file for data input here
Animal = data.animal.tolist()
Animalpattern = "|".join(str(v) for v in Animal)

Animalenv = data.animal_environment.tolist()
Animalenvpattern = "|".join(str(v) for v in Animalenv)

Animalfece = data.animal_feces.tolist()
Animalfecepattern = "|".join(str(v) for v in Animalfece)

Cider = data.cider.tolist()
Ciderpattern = "|".join(str(v) for v in Cider)

Dairy = data.dairy.tolist()
Dairypattern = "|".join(str(v) for v in Dairy)

Egg = data.egg.tolist()
Eggpattern = "|".join(str(v) for v in Egg)

Farm = data.farm.tolist()
Farmpattern = "|".join(str(v) for v in Farm)

Farmsewg = data.farm_sewage.tolist()
Farmsewgpattern = "|".join(str(v) for v in Farmsewg)

Farmwatr = data.farm_water.tolist()
Farmwatrpattern = "|".join(str(v) for v in Farmwatr)

Flour = data.flour.tolist()
Flourpattern = "|".join(str(v) for v in Flour)

Food = data.food.tolist()
Foodpattern = "|".join(str(v) for v in Food)

Fruitveg = data.fruit_vegetables.tolist()
Fruitvegpattern = "|".join(str(v) for v in Fruitveg)

insect = data.insect.tolist()
Insectpattern = "|".join(str(v) for v in insect)

Meat = data.meat.tolist()
Meatpattern = "|".join(str(v) for v in Meat)

Nuts = data.nuts.tolist()
Nutspattern = "|".join(str(v) for v in Nuts)

Fishseaf = data.fish_seafood.tolist()
Fishseafpattern = "|".join(str(v) for v in Fishseaf)

seeds = data.seeds.tolist()
Seedspattern = "|".join(str(v) for v in seeds)

Spice = data.spice_herbs.tolist()
Spicepattern = "|".join(str(v) for v in Spice)

Sewage = data.sewage.tolist()
Sewagepattern = "|".join(str(v) for v in Sewage)

Slaughterhouse = data.slaughterhouse_processing.tolist()
Slaughterhousepattern = "|".join(str(v) for v in Slaughterhouse)

Plant = data.plant.tolist()
Plantpattern = "|".join(str(v) for v in Plant)

Wastewater = data.wastewater.tolist()
Wastewaterpattern = "|".join(str(v) for v in Wastewater)

Water = data.water.tolist()
Waterpattern = "|".join(str(v) for v in Water)

Reptile = data.reptile.tolist()
Reptilepattern = "|".join(str(v) for v in Reptile)

Tea = data.tea.tolist()
Teapattern = "|".join(str(v) for v in Tea)

#file that will be read and have sources parsed from
InputCSV_NCBI = pandas.read_csv(args.infile)

InputCSV_NCBI['Animal'] = InputCSV_NCBI['isolation_source'].str.match(Animalpattern)
InputCSV_NCBI['Animal'] = InputCSV_NCBI['Animal'].map({True: 'Animal', False: ''})

InputCSV_NCBI['Animalenv'] = InputCSV_NCBI['isolation_source'].str.match(Animalenvpattern)
InputCSV_NCBI['Animalenv'] = InputCSV_NCBI['Animalenv'].map({True: 'Animal environment', False: ''})

InputCSV_NCBI['Animalfece'] = InputCSV_NCBI['isolation_source'].str.match(Animalfecepattern)
InputCSV_NCBI['Animalfece'] = InputCSV_NCBI['Animalfece'].map({True: 'Animal feces', False: ''})

InputCSV_NCBI['Cider'] = InputCSV_NCBI['isolation_source'].str.match(Ciderpattern)
InputCSV_NCBI['Cider'] = InputCSV_NCBI['Cider'].map({True: 'Cider', False: ''})

InputCSV_NCBI['Dairy'] = InputCSV_NCBI['isolation_source'].str.match(Dairypattern)
InputCSV_NCBI['Dairy'] = InputCSV_NCBI['Dairy'].map({True: 'Dairy', False: ''})

InputCSV_NCBI['Egg'] = InputCSV_NCBI['isolation_source'].str.match(Eggpattern)
InputCSV_NCBI['Egg'] = InputCSV_NCBI['Egg'].map({True: 'Egg', False: ''})

InputCSV_NCBI['Farm'] = InputCSV_NCBI['isolation_source'].str.match(Farmpattern)
InputCSV_NCBI['Farm'] = InputCSV_NCBI['Farm'].map({True: 'Farm', False: ''})

InputCSV_NCBI['Farmsewg'] = InputCSV_NCBI['isolation_source'].str.match(Farmsewgpattern)
InputCSV_NCBI['Farmsewg'] = InputCSV_NCBI['Farmsewg'].map({True: 'Farm sewage', False: ''})

InputCSV_NCBI['Farmwatr'] = InputCSV_NCBI['isolation_source'].str.match(Farmwatrpattern)
InputCSV_NCBI['Farmwatr'] = InputCSV_NCBI['Farmwatr'].map({True: 'Farm water', False: ''})

InputCSV_NCBI['Farmwatr'] = InputCSV_NCBI['isolation_source'].str.match(Farmwatrpattern)
InputCSV_NCBI['Farmwatr'] = InputCSV_NCBI['Farmwatr'].map({True: 'Farm water', False: ''})

InputCSV_NCBI['Flour'] = InputCSV_NCBI['isolation_source'].str.match(Flourpattern)
InputCSV_NCBI['Flour'] = InputCSV_NCBI['Flour'].map({True: 'Flour', False: ''})

InputCSV_NCBI['Food'] = InputCSV_NCBI['isolation_source'].str.match(Foodpattern)
InputCSV_NCBI['Food'] = InputCSV_NCBI['Food'].map({True: 'Food', False: ''})

InputCSV_NCBI['Fruitveg'] = InputCSV_NCBI['isolation_source'].str.match(Fruitvegpattern)
InputCSV_NCBI['Fruitveg'] = InputCSV_NCBI['Fruitveg'].map({True: 'Fruit/vegetables', False: ''})

InputCSV_NCBI['Insect'] = InputCSV_NCBI['isolation_source'].str.match(Insectpattern)
InputCSV_NCBI['Insect'] = InputCSV_NCBI['Insect'].map({True: 'Insect', False: ''})

InputCSV_NCBI['Meat'] = InputCSV_NCBI['isolation_source'].str.match(Meatpattern)
InputCSV_NCBI['Meat'] = InputCSV_NCBI['Meat'].map({True: 'Meat', False: ''})

InputCSV_NCBI['Nuts'] = InputCSV_NCBI['isolation_source'].str.match(Nutspattern)
InputCSV_NCBI['Nuts'] = InputCSV_NCBI['Nuts'].map({True: 'Nuts', False: ''})

InputCSV_NCBI['Fishseaf'] = InputCSV_NCBI['isolation_source'].str.match(Fishseafpattern)
InputCSV_NCBI['Fishseaf'] = InputCSV_NCBI['Fishseaf'].map({True: 'Fish/Seafood', False: ''})

InputCSV_NCBI['Sewage'] = InputCSV_NCBI['isolation_source'].str.match(Sewagepattern)
InputCSV_NCBI['Sewage'] = InputCSV_NCBI['Sewage'].map({True: 'Sewage', False: ''})

InputCSV_NCBI['SpiceHerbs'] = InputCSV_NCBI['isolation_source'].str.match(Spicepattern)
InputCSV_NCBI['SpiceHerbs'] = InputCSV_NCBI['SpiceHerbs'].map({True: 'Spice_Herbs', False: ''})

InputCSV_NCBI['Slaughterhouse'] = InputCSV_NCBI['isolation_source'].str.match(Slaughterhousepattern)
InputCSV_NCBI['Slaughterhouse'] = InputCSV_NCBI['Slaughterhouse'].map({True: 'Slaughterhouse', False: ''})

InputCSV_NCBI['Seeds'] = InputCSV_NCBI['isolation_source'].str.match(Seedspattern)
InputCSV_NCBI['Seeds'] = InputCSV_NCBI['Seeds'].map({True: 'Seeds', False: ''})

InputCSV_NCBI['Plant'] = InputCSV_NCBI['isolation_source'].str.match(Plantpattern)
InputCSV_NCBI['Plant'] = InputCSV_NCBI['Plant'].map({True: 'Plant', False: ''})

InputCSV_NCBI['Wastewater'] = InputCSV_NCBI['isolation_source'].str.match(Wastewaterpattern)
InputCSV_NCBI['Wastewater'] = InputCSV_NCBI['Wastewater'].map({True: 'Wastewater', False: ''})

InputCSV_NCBI['Water'] = InputCSV_NCBI['isolation_source'].str.match(Waterpattern)
InputCSV_NCBI['Water'] = InputCSV_NCBI['Water'].map({True: 'Water', False: ''})

InputCSV_NCBI['Reptile'] = InputCSV_NCBI['isolation_source'].str.match(Reptilepattern)
InputCSV_NCBI['Reptile'] = InputCSV_NCBI['Reptile'].map({True: 'Reptile', False: ''})

InputCSV_NCBI['Tea'] = InputCSV_NCBI['isolation_source'].str.match(Teapattern)
InputCSV_NCBI['Tea'] = InputCSV_NCBI['Tea'].map({True: 'Tea', False: ''})

#replacing empty cells with NaN so can concatenate without worrying about extra commas
InputCSV_NCBI['Animal'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Animalenv'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Animalfece'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Cider'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Dairy'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Egg'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Farm'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Farmsewg'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Farmwatr'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Flour'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Food'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Fruitveg'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Insect'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Meat'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Nuts'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Fishseaf'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Sewage'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Slaughterhouse'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Seeds'].replace('', np.nan, inplace=True)
InputCSV_NCBI['SpiceHerbs'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Plant'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Wastewater'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Water'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Reptile'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Tea'].replace('', np.nan, inplace=True)

#create a new column that concatenates all of the parsed source information into one
InputCSV_NCBI['Source'] = InputCSV_NCBI[['Animal','Animalenv', 'Animalfece',
                                               'Cider', 'Dairy', 'Egg', 'Farm', 'Farmsewg', 'Farmwatr', 'Flour',
                                               'Food', 'Fruitveg', 'Insect','Meat', 'Nuts',
                                               'Fishseaf', 'Sewage', 'Slaughterhouse', 'Seeds', 'Plant',
                                                'Wastewater', 'SpiceHerbs',
                                               'Water', 'Reptile', 'Tea']].apply(lambda x: ','.join(x[x.notnull()]), axis=1)


#now do the same for AMR data
ag = pandas.read_csv('resistance_genes.csv')

agygenes = list(ag['agygenes'])
agypattern = "|".join(str(v) for v in agygenes)
print(agypattern)

blagenes = list(ag['blagenes'])
blapattern = "|".join(str(v) for v in blagenes)

fosgenes = list(ag['fosgenes'])
fospattern = "|".join(str(v) for v in fosgenes)

MLSgenes = list(ag['MLS'])
MLSpattern = "|".join(str(v) for v in MLSgenes)

macrgenes = list(ag['macr'])
macrpattern = "|".join(str(v) for v in macrgenes)

LINgenes = list(ag['Lincosamide'])
LINpattern = "|".join(str(v) for v in LINgenes)

LSgenes = list(ag['LincosamideStreptogramin'])
LSpattern = "|".join(str(v) for v in LSgenes)

strggenes = list(ag['streptogramin'])
strgpattern = "|".join(str(v) for v in strggenes)

phegenes = list(ag['phegenes'])
phepattern = "|".join(str(v) for v in phegenes)

polgenes = list(ag['polgenes'])
polpattern = "|".join(str(v) for v in polgenes)

qngenes = list(ag['qngenes'])
qnpattern = "|".join(str(v) for v in qngenes)

sulgenes = list(ag['sulgenes'])
sulpattern = "|".join(str(v) for v in sulgenes)

tetgenes = list(ag['tetgenes'])
tetpattern = "|".join(str(v) for v in tetgenes)

dfrgenes = list(ag['dfrgenes'])
dfrpattern = "|".join(str(v) for v in dfrgenes)

glycgenes = list(ag['glycgenes'])
glycpattern = "|".join(str(v) for v in glycgenes)

AMRflux = list(ag['AMR-Efflux'])
AMRfluxpattern = "|".join(str(v) for v in AMRflux)

BIOCIDEflux = list(ag['Biocide-Efflux'])
BCDfluxpattern = "|".join(str(v) for v in BIOCIDEflux)

QACgenes = list(ag['QAC'])
QACpattern = "|".join(str(v) for v in QACgenes)

MTLgenes = list(ag['Metal-Resistance'])
MTLpattern = "|".join(str(v) for v in MTLgenes)

#now read the AMR data from the NCBI sheet
InputCSV_NCBI['aminoglycoside'] = InputCSV_NCBI['AMR_genotypes'].str.contains(agypattern)
InputCSV_NCBI['aminoglycoside'] = InputCSV_NCBI['aminoglycoside'].map({True: 'aminoglycoside', False: ''})

InputCSV_NCBI['betalactam'] = InputCSV_NCBI['AMR_genotypes'].str.contains(blapattern)
InputCSV_NCBI['betalactam'] = InputCSV_NCBI['betalactam'].map({True: 'betalactam', False: ''})

InputCSV_NCBI['fosfomycin'] = InputCSV_NCBI['AMR_genotypes'].str.contains(fospattern)
InputCSV_NCBI['fosfomycin'] = InputCSV_NCBI['fosfomycin'].map({True: 'fosfomycin', False: ''})

InputCSV_NCBI['MLS'] = InputCSV_NCBI['AMR_genotypes'].str.contains(MLSpattern)
InputCSV_NCBI['MLS'] = InputCSV_NCBI['MLS'].map({True: 'MLS', False: ''})

InputCSV_NCBI['macrolide'] = InputCSV_NCBI['AMR_genotypes'].str.contains(macrpattern)
InputCSV_NCBI['macrolide'] = InputCSV_NCBI['macrolide'].map({True: 'macrolide', False: ''})

InputCSV_NCBI['lincosamide'] = InputCSV_NCBI['AMR_genotypes'].str.contains(LINpattern)
InputCSV_NCBI['lincosamide'] = InputCSV_NCBI['lincosamide'].map({True: 'lincosamide', False: ''})

InputCSV_NCBI['LS'] = InputCSV_NCBI['AMR_genotypes'].str.contains(LSpattern)
InputCSV_NCBI['LS'] = InputCSV_NCBI['LS'].map({True: 'lincosamide/streptogramin', False: ''})

InputCSV_NCBI['streptogramin'] = InputCSV_NCBI['AMR_genotypes'].str.contains(strgpattern)
InputCSV_NCBI['streptogramin'] = InputCSV_NCBI['streptogramin'].map({True: 'streptogramin', False: ''})

InputCSV_NCBI['phenicol'] = InputCSV_NCBI['AMR_genotypes'].str.contains(phepattern)
InputCSV_NCBI['phenicol'] = InputCSV_NCBI['phenicol'].map({True: 'phenicol', False: ''})

InputCSV_NCBI['polymyxin'] = InputCSV_NCBI['AMR_genotypes'].str.contains(polpattern)
InputCSV_NCBI['polymyxin'] = InputCSV_NCBI['polymyxin'].map({True: 'polymyxin', False: ''})

InputCSV_NCBI['quinolone'] = InputCSV_NCBI['AMR_genotypes'].str.contains(qnpattern)
InputCSV_NCBI['quinolone'] = InputCSV_NCBI['quinolone'].map({True: 'quinolone', False: ''})

InputCSV_NCBI['sulphonamide'] = InputCSV_NCBI['AMR_genotypes'].str.contains(sulpattern)
InputCSV_NCBI['sulphonamide'] = InputCSV_NCBI['sulphonamide'].map({True: 'sulphonamide', False: ''})

InputCSV_NCBI['tetracycline'] = InputCSV_NCBI['AMR_genotypes'].str.contains(tetpattern)
InputCSV_NCBI['tetracycline'] = InputCSV_NCBI['tetracycline'].map({True: 'tetracycline', False: ''})

InputCSV_NCBI['trimethoprim'] = InputCSV_NCBI['AMR_genotypes'].str.contains(dfrpattern)
InputCSV_NCBI['trimethoprim'] = InputCSV_NCBI['trimethoprim'].map({True: 'trimethoprim', False: ''})

InputCSV_NCBI['glycopeptide'] = InputCSV_NCBI['AMR_genotypes'].str.contains(glycpattern)
InputCSV_NCBI['glycopeptide'] = InputCSV_NCBI['glycopeptide'].map({True: 'glycopeptide', False: ''})

InputCSV_NCBI['AMR-efflux'] = InputCSV_NCBI['AMR_genotypes'].str.contains(AMRfluxpattern)
InputCSV_NCBI['AMR-efflux'] = InputCSV_NCBI['AMR-efflux'].map({True: 'AMR-efflux', False: ''})

InputCSV_NCBI['Biocide-efflux'] = InputCSV_NCBI['stress_genotypes'].str.contains(BCDfluxpattern)
InputCSV_NCBI['Biocide-efflux'] = InputCSV_NCBI['Biocide-efflux'].map({True: 'Biocide-efflux', False: ''})

InputCSV_NCBI['QAC'] = InputCSV_NCBI['stress_genotypes'].str.contains(QACpattern)
InputCSV_NCBI['QAC'] = InputCSV_NCBI['QAC'].map({True: 'QAC', False: ''})

InputCSV_NCBI['Metal'] = InputCSV_NCBI['stress_genotypes'].str.contains(MTLpattern)
InputCSV_NCBI['Metal'] = InputCSV_NCBI['Metal'].map({True: 'Metal', False: ''})

#replace empty cells with NaN so can concatenate without worrying about extra commas
InputCSV_NCBI['aminoglycoside'].replace('', np.nan, inplace=True)
InputCSV_NCBI['betalactam'].replace('', np.nan, inplace=True)
InputCSV_NCBI['fosfomycin'].replace('', np.nan, inplace=True)
InputCSV_NCBI['MLS'].replace('', np.nan, inplace=True)
InputCSV_NCBI['macrolide'].replace('', np.nan, inplace=True)
InputCSV_NCBI['lincosamide'].replace('', np.nan, inplace=True)
InputCSV_NCBI['LS'].replace('', np.nan, inplace=True)
InputCSV_NCBI['phenicol'].replace('', np.nan, inplace=True)
InputCSV_NCBI['polymyxin'].replace('', np.nan, inplace=True)
InputCSV_NCBI['quinolone'].replace('', np.nan, inplace=True)
InputCSV_NCBI['streptogramin'].replace('', np.nan, inplace=True)
InputCSV_NCBI['sulphonamide'].replace('', np.nan, inplace=True)
InputCSV_NCBI['tetracycline'].replace('', np.nan, inplace=True)
InputCSV_NCBI['trimethoprim'].replace('', np.nan, inplace=True)
InputCSV_NCBI['glycopeptide'].replace('', np.nan, inplace=True)

#create a new column that concatenates all of the parsed antibiotic class information into one
InputCSV_NCBI['Antibiotic_Class'] = InputCSV_NCBI[['aminoglycoside', 'betalactam', 'fosfomycin', 'MLS', 'macrolide', 'lincosamide', 'LS',
                         'phenicol', 'polymyxin', 'quinolone', 'streptogramin', 'sulphonamide', 'tetracycline',
                         'trimethoprim', 'glycopeptide']].apply(lambda x: ','.join(x[x.notnull()]), axis=1)


#output a new csv file with source and AMR-class data
InputCSV_NCBI.to_csv(args.outfile)