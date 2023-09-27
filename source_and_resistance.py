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
#parser = argparse.ArgumentParser(description='NCBI Source and Antibiotic Class Parser. '
#                                             'Input and output should be in csv format. '
#                                             'If using metadata files from NCBI PathogenFinder FTP, do not forget to remove the "#" in the first line. '
#                                             'The "resistance_genes.csv" and "sources.csv" files must be in the same directory as this python script. '
#                                             'Source database last updated: 2021-04-20')
parser = argparse.ArgumentParser(description='details',
         usage='use "%(prog)s --help" for more information',
         formatter_class=argparse.RawTextHelpFormatter)
#parser.add_argument('-db', dest='database_file', type=str, required=True, help="""source database file.csv""")
parser.add_argument('--info', default=None,
                    help='''
                    NCBI Source and Resistance Assignment
                    Please cite "Cooper et al., INSERT CITATION"
                    
                    Input and output should be in csv format
                    If using metadata files from NCBI PathogenFinder FTP, do not forget to remove the "#" in the first line
                    The "resistance_genes.csv" and "sources.csv" files must be in the same directory as this python script
                    Source database last updated: 2021-04-20 (see README for more details)
                    ''')
parser.add_argument('-i', dest='infile', type=str, required=True, help="""Input Filename.csv""")
parser.add_argument('-o', dest='outfile', type=str, default="out_source_parser", help="""Output Filename.csv""")
argcomplete.autocomplete(parser)
args = parser.parse_args()

#read in the sources database file
data = pandas.read_csv('sources_IFSAC.csv')

#this is my first ever python code. I'm sure there is a more efficient way to do this (call row using pandas??)... but it currently serves its purpose...
#use the column headers in the IFSAC source database file for data input here
Animal = data.animal.tolist()
Animalpattern = "|".join(str(v) for v in Animal)

Animalfeed = data.animalfeed.tolist()
Animalfeedpattern = "|".join(str(v) for v in Animalfeed)

Animalenv = data.animalenvironment.tolist()
Animalenvpattern = "|".join(str(v) for v in Animalenv)

Dairy = data.dairy.tolist()
Dairypattern = "|".join(str(v) for v in Dairy)

Egg = data.egg.tolist()
Eggpattern = "|".join(str(v) for v in Egg)

Fishegg = data.fishegg.tolist()
Fisheggpattern = "|".join(str(v) for v in Fishegg)

Food = data.multiingredient.tolist()
Foodpattern = "|".join(str(v) for v in Food)

Foodprocessing = data.environmentalfactory.tolist()
Foodprocpattern ="|".join(str(v) for v in Foodprocessing)

Fruitveg = data.fruit_vegetables.tolist()
Fruitvegpattern = "|".join(str(v) for v in Fruitveg)

Meat = data.meatpoultry.tolist()
Meatpattern = "|".join(str(v) for v in Meat)

Nutsseeds = data.nutsseeds.tolist()
Nutsseedspattern = "|".join(str(v) for v in Nutsseeds)

Fishseaf = data.fish_seafood.tolist()
Fishseafpattern = "|".join(str(v) for v in Fishseaf)

Spice = data.herbs.tolist()
Spicepattern = "|".join(str(v) for v in Spice)

#file that will be read and have sources parsed from
InputCSV_NCBI = pandas.read_csv(args.infile)

ifsaclist = InputCSV_NCBI.IFSAC_category.tolist()
if ifsaclist == []:
    print('IFSAC category is empty. Skipping.')
else:
    #print('Data found')

    InputCSV_NCBI['Animal'] = InputCSV_NCBI['IFSAC_category'].str.match(Animalpattern)
    InputCSV_NCBI['Animal'] = InputCSV_NCBI['Animal'].map({True: 'Animal', False: ''})

    InputCSV_NCBI['Animalenv'] = InputCSV_NCBI['IFSAC_category'].str.match(Animalenvpattern)
    InputCSV_NCBI['Animalenv'] = InputCSV_NCBI['Animalenv'].map({True: 'Animal environment', False: ''})

    InputCSV_NCBI['Animalfeed'] = InputCSV_NCBI['IFSAC_category'].str.match(Animalfeedpattern)
    InputCSV_NCBI['Animalfeed'] = InputCSV_NCBI['Animalfeed'].map({True: 'Animal feed', False: ''})

    InputCSV_NCBI['Dairy'] = InputCSV_NCBI['IFSAC_category'].str.match(Dairypattern)
    InputCSV_NCBI['Dairy'] = InputCSV_NCBI['Dairy'].map({True: 'Dairy', False: ''})

    InputCSV_NCBI['Egg'] = InputCSV_NCBI['IFSAC_category'].str.match(Eggpattern)
    InputCSV_NCBI['Egg'] = InputCSV_NCBI['Egg'].map({True: 'Egg', False: ''})

    InputCSV_NCBI['Fishegg'] = InputCSV_NCBI['IFSAC_category'].str.match(Fisheggpattern)
    InputCSV_NCBI['Fishegg'] = InputCSV_NCBI['Fishegg'].map({True: 'Fish eggs', False: ''})

    InputCSV_NCBI['Food'] = InputCSV_NCBI['IFSAC_category'].str.match(Foodpattern)
    InputCSV_NCBI['Food'] = InputCSV_NCBI['Food'].map({True: 'Multi-product', False: ''})

    InputCSV_NCBI['Foodprocessing'] = InputCSV_NCBI['IFSAC_category'].str.match(Foodprocpattern)
    InputCSV_NCBI['Foodprocessing'] = InputCSV_NCBI['Foodprocessing'].map({True: 'Food processing environment', False: ''})

    InputCSV_NCBI['Fruitveg'] = InputCSV_NCBI['IFSAC_category'].str.match(Fruitvegpattern)
    InputCSV_NCBI['Fruitveg'] = InputCSV_NCBI['Fruitveg'].map({True: 'Fruit/Vegetables', False: ''})

    InputCSV_NCBI['Meat'] = InputCSV_NCBI['IFSAC_category'].str.match(Meatpattern)
    InputCSV_NCBI['Meat'] = InputCSV_NCBI['Meat'].map({True: 'Meat/Poultry', False: ''})

    InputCSV_NCBI['Nutsseeds'] = InputCSV_NCBI['IFSAC_category'].str.match(Nutsseedspattern)
    InputCSV_NCBI['Nutsseeds'] = InputCSV_NCBI['Nutsseeds'].map({True: 'Nuts/Seeds', False: ''})

    InputCSV_NCBI['Fishseaf'] = InputCSV_NCBI['IFSAC_category'].str.match(Fishseafpattern)
    InputCSV_NCBI['Fishseaf'] = InputCSV_NCBI['Fishseaf'].map({True: 'Fish/Seafood', False: ''})

    InputCSV_NCBI['SpiceHerbs'] = InputCSV_NCBI['IFSAC_category'].str.match(Spicepattern)
    InputCSV_NCBI['SpiceHerbs'] = InputCSV_NCBI['SpiceHerbs'].map({True: 'Spice/Herbs', False: ''})


    #replacing empty cells with NaN so can concatenate without worrying about extra commas
    InputCSV_NCBI['Animal'].replace('', np.nan, inplace=True)
    InputCSV_NCBI['Animalenv'].replace('', np.nan, inplace=True)
    InputCSV_NCBI['Animalfeed'].replace('', np.nan, inplace=True)
    InputCSV_NCBI['Dairy'].replace('', np.nan, inplace=True)
    InputCSV_NCBI['Egg'].replace('', np.nan, inplace=True)
    InputCSV_NCBI['Fishegg'].replace('', np.nan, inplace=True)
    InputCSV_NCBI['Food'].replace('', np.nan, inplace=True)
    InputCSV_NCBI['Foodprocessing'].replace('', np.nan, inplace=True)
    InputCSV_NCBI['Fruitveg'].replace('', np.nan, inplace=True)
    InputCSV_NCBI['Meat'].replace('', np.nan, inplace=True)
    InputCSV_NCBI['Nutsseeds'].replace('', np.nan, inplace=True)
    InputCSV_NCBI['Fishseaf'].replace('', np.nan, inplace=True)
    InputCSV_NCBI['SpiceHerbs'].replace('', np.nan, inplace=True)



    #create a new column that concatenates all of the parsed source IFSAC information into one
    InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI[['Animal','Animalenv', 'Animalfeed',
                                                   'Dairy', 'Egg', 'Fishegg',
                                                   'Food', 'Fruitveg', 'Foodprocessing','Meat', 'Nutsseeds',
                                                   'Fishseaf', 'SpiceHerbs']].apply(lambda x: ','.join(x[x.notnull()]), axis=1)

    #remove all of the extra columns I made
    InputCSV_NCBI = InputCSV_NCBI.drop(['Animal','Animalenv', 'Animalfeed',
                                                   'Dairy', 'Egg', 'Fishegg',
                                                   'Food', 'Fruitveg', 'Foodprocessing','Meat', 'Nutsseeds',
                                                   'Fishseaf', 'SpiceHerbs'], axis=1)

#now search through the source_IFSAC column and replace anything with commas
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal,Meat/Poultry,Food processing environment','Food processing environment')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal,Multi-product,Meat/Poultry','Multi-product')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal,Animal feces,Dairy','Animal feces')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal,Animal feces,Farm','Farm')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Sewage,Wastewater,Water','Wastewater')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal,Animal feces','Animal feces')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal,Multi-product','Multi-product')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal,Dairy','Dairy')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal,Egg','Egg')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Dairy,Water','Dairy')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal,Meat/Poultry','Meat/Poultry')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Multi-product,Meat/Poultry','Multi-product')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Wastewater,Water','Wastewater')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Fruit/Vegetables,Nuts/Seeds','Nuts/Seeds')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Dairy,Farm','Farm')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal,Farm','Farm')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Farm sewage,Sewage','Farm sewage')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Sewage,Food processing environment','Food processing environment')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Fruit/Vegetables,Water','Farm water')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal,Reptile','Reptile')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Sewage,Water','Sewage')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Fruit/Vegetables,Meat/Poultry','Meat/Poultry')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Aquatic,Water','Aquatic')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal feces,Farm','Farm')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal,Farm water','Farm water')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Farm water,Water','Farm water')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Fruit/Vegetables,Plant','Plant')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Multi-product,Fruit/Vegetables','Multi-product')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal,Farm sewage','Farm sewage')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Fruit/Vegetables,Spice/Herbs','Spice/Herbs')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal feces,Meat/Poultry','Animal feces')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal,Fish/Seafood','Fish/Seafood')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Farm,Farm sewage','Farm sewage')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Multi-product,Food processing environment','Food processing environment')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal feces,Dairy','Animal feces')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Farm water,Meat/Poultry','Farm water')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Food processing environment,Water','Food processing environment')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal,Food processing environment','Food processing environment')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Farm,Insect','Insect')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Farm,Meat/Poultry','Farm')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal feed,Meat/Poultry','Animal feed')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Sewage,Wastewater','Wastewater')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal feces,Animal feed','Animal feces')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal feed,Farm','Farm')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Meat/Poultry,Food processing environment','Food processing environment')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Dairy,Multi-product','Multi-product')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Dairy,Fruit/Vegetables','Fruit/Vegetables')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Dairy,Food processing environment','Food processing environment')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Egg,Meat/Poultry','Egg')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal,Animal feed','Animal feed')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal environment,Fish/Seafood','Animal environment')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Fish/Seafood,Water','Fish/Seafood')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Aquatic,Reptile','Reptile')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal feed,Fruit/Vegetables','Animal feed')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal,Fruit/Vegetables','Fruit/Vegetables')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal environment,Water','Animal environment')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Egg,Multi-product','Multi-product')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Farm water,Fruit/Vegetables','Farm water')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Farm,Farm water','Farm water')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Fish eggs,Fish/Seafood','Fish/Seafood')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Fish/Seafood,Food processing environment','Food processing environment')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Food processing environment,Plant','Plant')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Fruit/Vegetables,Fish/Seafood','Fruit/Vegetables')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Fruit/Vegetables,Food processing environment','Food processing environment')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Multi-product,Fish/Seafood','Fish/Seafood')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Multi-product,Fruit/Vegetables','Multi-product')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Multi-product,Meat/Poultry','Multi-product')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Multi-product,Plant','Plant')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal envirnoment,Food processing environment','Food processing environment')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal feed,Multi-product','Animal feed')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal,Pet food','Pet food')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal feed,Food processing environment','Food processing environment')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Multi-product,Spice/Herbs','Spice/Herbs')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal,Spice/Herbs','Spice/Herbs')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Egg,Farm','Farm')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Multi-product,Nuts/Seeds','Multi-product')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Nuts/Seeds,Spice/Herbs','Spice/Herbs')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Fruit/Vegetables,Reptile','Reptile')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Animal feces,Insect','Animal feces')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Multi-product,Reptile','Reptile')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Fruit/Vegetables,Reptile','Reptile')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Aquatic,Meat/Poultry','Fish/Seafood')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Egg,Fish eggs','Fish/Seafood')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Farm,Food processing environment','Farm')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Farm,Fruit/Vegetables','Farm')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Farm,Multi-product','Farm')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Farm,Plant','Farm')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Nuts/Seeds,Food processing environment','Food processing environment')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Nuts/Seeds,Plant','Plant')
InputCSV_NCBI['Source_IFSAC'] = InputCSV_NCBI['Source_IFSAC'].str.replace('Plant,Spice/Herbs','Spice/Herbs')






#now do the same thing with the source data manually curated by Ashley Cooper
#read in the sources database file
source2 = pandas.read_csv('sources.csv')

#this is my first ever python code. I'm sure there is a more efficient way to do this, but it serves its purpose...
#use the column headers in the source database file for data input here
Animal = source2.animal.tolist()
Animalpattern = "|".join(str(v) for v in Animal)

Animalenv = source2.animal_environment.tolist()
Animalenvpattern = "|".join(str(v) for v in Animalenv)

Animalfece = source2.animal_feces.tolist()
Animalfecepattern = "|".join(str(v) for v in Animalfece)

Animalfeed = source2.Feed.tolist()
Animalfeedpattern = "|".join(str(v) for v in Animalfeed)

rawpetfood = source2.raw_pet_food.tolist()
rawpetfoodpattern = "|".join(str(v) for v in rawpetfood)

petfood = source2.pet_food.tolist()
petfoodpattern = "|".join(str(v) for v in petfood)

Aquatic = source2.aquatic.tolist()
Aquaticpattern = "|".join(str(v) for v in Aquatic)

Cider = source2.cider.tolist()
Ciderpattern = "|".join(str(v) for v in Cider)

Dairy = source2.dairy.tolist()
Dairypattern = "|".join(str(v) for v in Dairy)

Egg = source2.egg.tolist()
Eggpattern = "|".join(str(v) for v in Egg)

Farm = source2.farm.tolist()
Farmpattern = "|".join(str(v) for v in Farm)

Farmsewg = source2.farm_sewage.tolist()
Farmsewgpattern = "|".join(str(v) for v in Farmsewg)

Farmwatr = source2.farm_water.tolist()
Farmwatrpattern = "|".join(str(v) for v in Farmwatr)

Flour = source2.flour.tolist()
Flourpattern = "|".join(str(v) for v in Flour)

Food = source2.food.tolist()
Foodpattern = "|".join(str(v) for v in Food)

Fruitveg = source2.fruit_vegetables.tolist()
Fruitvegpattern = "|".join(str(v) for v in Fruitveg)

insect = source2.insect.tolist()
Insectpattern = "|".join(str(v) for v in insect)

Meat = source2.meat.tolist()
Meatpattern = "|".join(str(v) for v in Meat)

Nutsseeds = source2.nutsseeds.tolist()
Nutsseedspattern = "|".join(str(v) for v in Nutsseeds)

Fishseaf = source2.fish_seafood.tolist()
Fishseafpattern = "|".join(str(v) for v in Fishseaf)

#seeds = source2.seeds.tolist()
#Seedspattern = "|".join(str(v) for v in seeds)

Spice = source2.spice_herbs.tolist()
Spicepattern = "|".join(str(v) for v in Spice)

Sewage = source2.sewage.tolist()
Sewagepattern = "|".join(str(v) for v in Sewage)

Slaughterhouse = source2.slaughterhouse_processing.tolist()
Slaughterhousepattern = "|".join(str(v) for v in Slaughterhouse)

Plant = source2.plant.tolist()
Plantpattern = "|".join(str(v) for v in Plant)

Wastewater = source2.wastewater.tolist()
Wastewaterpattern = "|".join(str(v) for v in Wastewater)

Water = source2.water.tolist()
Waterpattern = "|".join(str(v) for v in Water)

Reptile = source2.reptile.tolist()
Reptilepattern = "|".join(str(v) for v in Reptile)

Tea = source2.tea.tolist()
Teapattern = "|".join(str(v) for v in Tea)

#file that will be read and have sources parsed from
#InputCSV_NCBI = pandas.read_csv(args.infile)

InputCSV_NCBI['Animal'] = InputCSV_NCBI['isolation_source'].str.match(Animalpattern)
InputCSV_NCBI['Animal'] = InputCSV_NCBI['Animal'].map({True: 'Animal', False: ''})

InputCSV_NCBI['Animalenv'] = InputCSV_NCBI['isolation_source'].str.match(Animalenvpattern)
InputCSV_NCBI['Animalenv'] = InputCSV_NCBI['Animalenv'].map({True: 'Animal environment', False: ''})

InputCSV_NCBI['Animalfece'] = InputCSV_NCBI['isolation_source'].str.match(Animalfecepattern)
InputCSV_NCBI['Animalfece'] = InputCSV_NCBI['Animalfece'].map({True: 'Animal feces', False: ''})

InputCSV_NCBI['Animalfeed'] = InputCSV_NCBI['isolation_source'].str.match(Animalfeedpattern)
InputCSV_NCBI['Animalfeed'] = InputCSV_NCBI['Animalfeed'].map({True: 'Animal feed', False: ''})

InputCSV_NCBI['raw_pet_food'] = InputCSV_NCBI['isolation_source'].str.match(rawpetfoodpattern)
InputCSV_NCBI['raw_pet_food'] = InputCSV_NCBI['raw_pet_food'].map({True: 'Raw pet food', False: ''})

InputCSV_NCBI['pet_food'] = InputCSV_NCBI['isolation_source'].str.match(petfoodpattern)
InputCSV_NCBI['pet_food'] = InputCSV_NCBI['pet_food'].map({True: 'Pet food', False: ''})

InputCSV_NCBI['Aquatic'] = InputCSV_NCBI['isolation_source'].str.match(Aquaticpattern)
InputCSV_NCBI['Aquatic'] = InputCSV_NCBI['Aquatic'].map({True: 'Aquatic', False: ''})

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

#InputCSV_NCBI['Farmwatr'] = InputCSV_NCBI['isolation_source'].str.match(Farmwatrpattern)
#InputCSV_NCBI['Farmwatr'] = InputCSV_NCBI['Farmwatr'].map({True: 'Farm water', False: ''})

InputCSV_NCBI['Flour'] = InputCSV_NCBI['isolation_source'].str.match(Flourpattern)
InputCSV_NCBI['Flour'] = InputCSV_NCBI['Flour'].map({True: 'Flour', False: ''})

InputCSV_NCBI['Food'] = InputCSV_NCBI['isolation_source'].str.match(Foodpattern)
InputCSV_NCBI['Food'] = InputCSV_NCBI['Food'].map({True: 'Multi-product', False: ''})

InputCSV_NCBI['Fruitveg'] = InputCSV_NCBI['isolation_source'].str.match(Fruitvegpattern)
InputCSV_NCBI['Fruitveg'] = InputCSV_NCBI['Fruitveg'].map({True: 'Fruit/Vegetables', False: ''})

InputCSV_NCBI['Insect'] = InputCSV_NCBI['isolation_source'].str.match(Insectpattern)
InputCSV_NCBI['Insect'] = InputCSV_NCBI['Insect'].map({True: 'Insect', False: ''})

InputCSV_NCBI['Meat'] = InputCSV_NCBI['isolation_source'].str.match(Meatpattern)
InputCSV_NCBI['Meat'] = InputCSV_NCBI['Meat'].map({True: 'Meat/Poultry', False: ''})

InputCSV_NCBI['Nutsseeds'] = InputCSV_NCBI['isolation_source'].str.match(Nutsseedspattern)
InputCSV_NCBI['Nutsseeds'] = InputCSV_NCBI['Nutsseeds'].map({True: 'Nuts/Seeds', False: ''})

InputCSV_NCBI['Fishseaf'] = InputCSV_NCBI['isolation_source'].str.match(Fishseafpattern)
InputCSV_NCBI['Fishseaf'] = InputCSV_NCBI['Fishseaf'].map({True: 'Fish/Seafood', False: ''})

InputCSV_NCBI['Sewage'] = InputCSV_NCBI['isolation_source'].str.match(Sewagepattern)
InputCSV_NCBI['Sewage'] = InputCSV_NCBI['Sewage'].map({True: 'Sewage', False: ''})

InputCSV_NCBI['SpiceHerbs'] = InputCSV_NCBI['isolation_source'].str.match(Spicepattern)
InputCSV_NCBI['SpiceHerbs'] = InputCSV_NCBI['SpiceHerbs'].map({True: 'Spice/Herbs', False: ''})

InputCSV_NCBI['Slaughterhouse'] = InputCSV_NCBI['isolation_source'].str.match(Slaughterhousepattern)
InputCSV_NCBI['Slaughterhouse'] = InputCSV_NCBI['Slaughterhouse'].map({True: 'Food processing environment', False: ''})

#InputCSV_NCBI['Seeds'] = InputCSV_NCBI['isolation_source'].str.match(Seedspattern)
#InputCSV_NCBI['Seeds'] = InputCSV_NCBI['Seeds'].map({True: 'Seeds', False: ''})

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
InputCSV_NCBI['Animalfeed'].replace('', np.nan, inplace=True)
InputCSV_NCBI['raw_pet_food'].replace('', np.nan, inplace=True)
InputCSV_NCBI['pet_food'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Aquatic'].replace('', np.nan, inplace=True)
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
InputCSV_NCBI['Nutsseeds'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Fishseaf'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Sewage'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Slaughterhouse'].replace('', np.nan, inplace=True)
#InputCSV_NCBI['Seeds'].replace('', np.nan, inplace=True)
InputCSV_NCBI['SpiceHerbs'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Plant'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Wastewater'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Water'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Reptile'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Tea'].replace('', np.nan, inplace=True)

#create a new column that concatenates all of the parsed source information into one
InputCSV_NCBI['Source2'] = InputCSV_NCBI[['Animal','Animalenv', 'Animalfece','Animalfeed', 'raw_pet_food','pet_food','Aquatic',
                                               'Cider', 'Dairy', 'Egg', 'Farm', 'Farmsewg', 'Farmwatr', 'Flour',
                                               'Food', 'Fruitveg', 'Insect','Meat', 'Nutsseeds',
                                               'Fishseaf', 'Sewage', 'Slaughterhouse', 'Plant',
                                                'Wastewater', 'SpiceHerbs',
                                               'Water', 'Reptile', 'Tea']].apply(lambda x: ','.join(x[x.notnull()]), axis=1)

#remove all of the extra columns I made
InputCSV_NCBI = InputCSV_NCBI.drop(['Animal','Animalenv', 'Animalfece', 'Animalfeed','raw_pet_food','pet_food','Aquatic',
                                               'Cider', 'Dairy', 'Egg', 'Farm', 'Farmsewg', 'Farmwatr', 'Flour',
                                               'Food', 'Fruitveg', 'Insect','Meat', 'Nutsseeds',
                                               'Fishseaf', 'Sewage', 'Slaughterhouse', 'Plant',
                                                'Wastewater', 'SpiceHerbs',
                                               'Water', 'Reptile', 'Tea'], axis=1)

#now search through the Source2 column and edit the entries with commas (eg Chicken egg may give Animal,Egg because both words in dictionary)
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal,Meat/Poultry,Food processing environment','Food processing environment')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal,Multi-product,Meat/Poultry','Multi-product')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal,Animal feces,Dairy','Animal feces')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal,Animal feces,Farm','Farm')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Sewage,Wastewater,Water','Wastewater')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal,Animal feces','Animal feces')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal,Multi-product','Multi-product')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal,Dairy','Dairy')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal,Egg','Egg')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Dairy,Water','Dairy')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal,Meat/Poultry','Meat/Poultry')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Multi-product,Meat/Poultry','Multi-product')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Wastewater,Water','Wastewater')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Fruit/Vegetables,Nuts/Seeds','Nuts/Seeds')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Dairy,Farm','Farm')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal,Farm','Farm')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Farm sewage,Sewage','Farm sewage')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Sewage,Food processing environment','Food processing environment')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Fruit/Vegetables,Water','Farm water')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal,Reptile','Reptile')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Sewage,Water','Sewage')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Fruit/Vegetables,Meat/Poultry','Meat/Poultry')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Aquatic,Water','Aquatic')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal feces,Farm','Farm')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal,Farm water','Farm water')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Farm water,Water','Farm water')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Fruit/Vegetables,Plant','Plant')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Multi-product,Fruit/Vegetables','Multi-product')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal,Farm sewage','Farm sewage')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Fruit/Vegetables,Spice/Herbs','Spice/Herbs')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal feces,Meat/Poultry','Animal feces')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal,Fish/Seafood','Fish/Seafood')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Farm,Farm sewage','Farm sewage')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Multi-product,Food processing environment','Food processing environment')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal feces,Dairy','Animal feces')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Farm water,Meat/Poultry','Farm water')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Food processing environment,Water','Food processing environment')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal,Food processing environment','Food processing environment')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Farm,Insect','Insect')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Farm,Meat/Poultry','Farm')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal feed,Meat/Poultry','Animal feed')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Sewage,Wastewater','Wastewater')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal feces,Animal feed','Animal feces')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal feed,Farm','Farm')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Raw pet food,Meat/Poultry','Raw pet food')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Pet food,Meat/Poultry','Pet food')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Meat/Poultry,Food processing environment','Food processing environment')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Dairy,Multi-product','Multi-product')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Dairy,Fruit/Vegetables','Fruit/Vegetables')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Dairy,Food processing environment','Food processing environment')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Egg,Meat/Poultry','Egg')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal,Animal feed','Animal feed')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal,Pet food','Pet food')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal,Raw pet food','Raw pet food')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal environment,Fish/Seafood','Animal environment')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Fish/Seafood,Water','Fish/Seafood')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Aquatic,Reptile','Reptile')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal feed,Fruit/Vegetables','Animal feed')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Raw pet food,Fruit/Vegetables','Raw pet food')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Pet food,Fruit/Vegetables','Pet food')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal feed,Fish/Seafood','Animal feed')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Raw pet food,Fish/Seafood','Raw pet food')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Pet food,Fish/Seafood','Pet food')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal,Fruit/Vegetables','Fruit/Vegetables')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal environment,Water','Animal environment')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Egg,Multi-product','Multi-product')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Farm water,Fruit/Vegetables','Farm water')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Farm,Farm water','Farm water')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Fish eggs,Fish/Seafood','Fish/Seafood')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Fish/Seafood,Food processing environment','Food processing environment')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Food processing environment,Plant','Plant')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Fruit/Vegetables,Fish/Seafood','Fruit/Vegetables')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Fruit/Vegetables,Food processing environment','Food processing environment')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Multi-product,Fish/Seafood','Fish/Seafood')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Multi-product,Fruit/Vegetables','Multi-product')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Multi-product,Meat/Poultry','Multi-product')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Multi-product,Plant','Plant')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal envirnoment,Food processing environment','Food processing environment')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal feed,Multi-product','Animal feed')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal feed,Food processing environment','Food processing environment')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Multi-product,Spice/Herbs','Spice/Herbs')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal,Spice/Herbs','Spice/Herbs')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Egg,Farm','Farm')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Multi-product,Nuts/Seeds','Multi-product')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Nuts/Seeds,Spice/Herbs','Spice/Herbs')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Fruit/Vegetables,Reptile','Reptile')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Animal feces,Insect','Animal feces')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Multi-product,Reptile','Reptile')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Fruit/Vegetables,Reptile','Reptile')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Aquatic,Meat/Poultry','Fish/Seafood')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Egg,Fish eggs','Fish/Seafood')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Farm,Food processing environment','Farm')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Farm,Fruit/Vegetables','Farm')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Farm,Multi-product','Farm')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Farm,Plant','Farm')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Nuts/Seeds,Food processing environment','Food processing environment')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Nuts/Seeds,Plant','Plant')
InputCSV_NCBI['Source2'] = InputCSV_NCBI['Source2'].str.replace('Plant,Spice/Herbs','Spice/Herbs')





#now do the same for resistance data
ag = pandas.read_csv('resistance_genes.csv')

agygenes = list(ag['agygenes'])
agypattern = "|".join(str(v) for v in agygenes)
#print(agypattern)

blagenes = list(ag['blagenes'])
blapattern = "|".join(str(v) for v in blagenes)

bleogenes = list(ag['bleomycin'])
bleopattern = "|".join(str(v) for v in bleogenes)

fosgenes = list(ag['fosgenes'])
fospattern = "|".join(str(v) for v in fosgenes)

fusidgenes = list(ag['fusidicacid'])
fusidpattern = "|".join(str(v) for v in fusidgenes)

glycgenes = list(ag['glycgenes'])
glycpattern = "|".join(str(v) for v in glycgenes)

MLSgenes = list(ag['MLS'])
MLSpattern = "|".join(str(v) for v in MLSgenes)

macrgenes = list(ag['macr'])
macrpattern = "|".join(str(v) for v in macrgenes)

LINgenes = list(ag['Lincosamide'])
LINpattern = "|".join(str(v) for v in LINgenes)

LSgenes = list(ag['LincosamideStreptogramin'])
LSpattern = "|".join(str(v) for v in LSgenes)

mupigenes = list(ag['mupirocin'])
mupipattern = "|".join(str(v) for v in mupigenes)

nitrogenes = list(ag['nitroimidazole'])
nitropattern = "|".join(str(v) for v in nitrogenes)

phegenes = list(ag['phegenes'])
phepattern = "|".join(str(v) for v in phegenes)

pheoxagenes = list(ag['phenicol_oxazolidinone'])
pheoxapattern = "|".join(str(v) for v in pheoxagenes)

plurgenes = list(ag['pluromutilin'])
plurpattern = "|".join(str(v) for v in plurgenes)

phequingenes = list(ag['phenicol_quinolone'])
phequinpattern = "|".join(str(v) for v in phequingenes)

polgenes = list(ag['polgenes'])
polpattern = "|".join(str(v) for v in polgenes)

qngenes = list(ag['qngenes'])
qnpattern = "|".join(str(v) for v in qngenes)

rifgenes = list(ag['rifamycin'])
rifpattern = "|".join(str(v) for v in rifgenes)

strggenes = list(ag['streptogramin'])
strgpattern = "|".join(str(v) for v in strggenes)

strthrggenes = list(ag['streptothricin'])
strthrgpattern = "|".join(str(v) for v in strthrggenes)

sulgenes = list(ag['sulgenes'])
sulpattern = "|".join(str(v) for v in sulgenes)

tetmygenes = list(ag['tetracenomycin'])
tetmypattern = "|".join(str(v) for v in tetmygenes)

tetgenes = list(ag['tetgenes'])
tetpattern = "|".join(str(v) for v in tetgenes)

thiogenes = list(ag['thiostrepton'])
thiopattern = "|".join(str(v) for v in thiogenes)

dfrgenes = list(ag['dfrgenes'])
dfrpattern = "|".join(str(v) for v in dfrgenes)

tubrgenes = list(ag['tuberactinomycin'])
tubrpattern = "|".join(str(v) for v in tubrgenes)

AMRflux = list(ag['AMR-Efflux'])
AMRfluxpattern = "|".join(str(v) for v in AMRflux)

BIOCIDEflux = list(ag['Biocide-Efflux'])
BCDfluxpattern = "|".join(str(v) for v in BIOCIDEflux)

biocidegenes = list(ag['biocide'])
biocidepattern = "|".join(str(v) for v in biocidegenes)

MTLgenes = list(ag['Metal-Resistance'])
MTLpattern = "|".join(str(v) for v in MTLgenes)

#now read the resistance data from the NCBI sheet
InputCSV_NCBI['aminoglycoside'] = InputCSV_NCBI['AMR_genotypes'].str.contains(agypattern)
InputCSV_NCBI['aminoglycoside'] = InputCSV_NCBI['aminoglycoside'].map({True: 'aminoglycoside', False: ''})

InputCSV_NCBI['betalactam'] = InputCSV_NCBI['AMR_genotypes'].str.contains(blapattern)
InputCSV_NCBI['betalactam'] = InputCSV_NCBI['betalactam'].map({True: 'betalactam', False: ''})

InputCSV_NCBI['bleomycin'] = InputCSV_NCBI['AMR_genotypes'].str.contains(bleopattern)
InputCSV_NCBI['bleomycin'] = InputCSV_NCBI['bleomycin'].map({True: 'bleomycin', False: ''})

InputCSV_NCBI['fosfomycin'] = InputCSV_NCBI['AMR_genotypes'].str.contains(fospattern)
InputCSV_NCBI['fosfomycin'] = InputCSV_NCBI['fosfomycin'].map({True: 'fosfomycin', False: ''})

InputCSV_NCBI['fusidic acid'] = InputCSV_NCBI['AMR_genotypes'].str.contains(fusidpattern)
InputCSV_NCBI['fusidic acid'] = InputCSV_NCBI['fusidic acid'].map({True: 'fusidic acid', False: ''})

InputCSV_NCBI['glycopeptide'] = InputCSV_NCBI['AMR_genotypes'].str.contains(glycpattern)
InputCSV_NCBI['glycopeptide'] = InputCSV_NCBI['glycopeptide'].map({True: 'glycopeptide', False: ''})

InputCSV_NCBI['MLS'] = InputCSV_NCBI['AMR_genotypes'].str.contains(MLSpattern)
InputCSV_NCBI['MLS'] = InputCSV_NCBI['MLS'].map({True: 'MLS', False: ''})

InputCSV_NCBI['macrolide'] = InputCSV_NCBI['AMR_genotypes'].str.contains(macrpattern)
InputCSV_NCBI['macrolide'] = InputCSV_NCBI['macrolide'].map({True: 'macrolide', False: ''})

InputCSV_NCBI['lincosamide'] = InputCSV_NCBI['AMR_genotypes'].str.contains(LINpattern)
InputCSV_NCBI['lincosamide'] = InputCSV_NCBI['lincosamide'].map({True: 'lincosamide', False: ''})

InputCSV_NCBI['lincosamide_streptogramin'] = InputCSV_NCBI['AMR_genotypes'].str.contains(LSpattern)
InputCSV_NCBI['lincosamide_streptogramin'] = InputCSV_NCBI['lincosamide_streptogramin'].map({True: 'lincosamide_streptogramin', False: ''})

InputCSV_NCBI['mupirocin'] = InputCSV_NCBI['AMR_genotypes'].str.contains(mupipattern)
InputCSV_NCBI['mupirocin'] = InputCSV_NCBI['mupirocin'].map({True: 'mupirocin', False: ''})

InputCSV_NCBI['nitroimidazole'] = InputCSV_NCBI['AMR_genotypes'].str.contains(nitropattern)
InputCSV_NCBI['nitroimidazole'] = InputCSV_NCBI['nitroimidazole'].map({True: 'nitroimidazole', False: ''})

InputCSV_NCBI['phenicol'] = InputCSV_NCBI['AMR_genotypes'].str.contains(phepattern)
InputCSV_NCBI['phenicol'] = InputCSV_NCBI['phenicol'].map({True: 'phenicol', False: ''})

InputCSV_NCBI['phenicol_oxazolidinone'] = InputCSV_NCBI['AMR_genotypes'].str.contains(pheoxapattern)
InputCSV_NCBI['phenicol_oxazolidinone'] = InputCSV_NCBI['phenicol_oxazolidinone'].map({True: 'phenicol_oxazolidinone', False: ''})

InputCSV_NCBI['phenicol_quinolone'] = InputCSV_NCBI['AMR_genotypes'].str.contains(phequinpattern)
InputCSV_NCBI['phenicol_quinolone'] = InputCSV_NCBI['phenicol_quinolone'].map({True: 'phenicol_quinolone', False: ''})

InputCSV_NCBI['pluromutilin'] = InputCSV_NCBI['AMR_genotypes'].str.contains(plurpattern)
InputCSV_NCBI['pluromutilin'] = InputCSV_NCBI['pluromutilin'].map({True: 'pluromutilin', False: ''})

InputCSV_NCBI['polymyxin'] = InputCSV_NCBI['AMR_genotypes'].str.contains(polpattern)
InputCSV_NCBI['polymyxin'] = InputCSV_NCBI['polymyxin'].map({True: 'polymyxin', False: ''})

InputCSV_NCBI['quinolone'] = InputCSV_NCBI['AMR_genotypes'].str.contains(qnpattern)
InputCSV_NCBI['quinolone'] = InputCSV_NCBI['quinolone'].map({True: 'quinolone', False: ''})

InputCSV_NCBI['rifamycin'] = InputCSV_NCBI['AMR_genotypes'].str.contains(rifpattern)
InputCSV_NCBI['rifamycin'] = InputCSV_NCBI['rifamycin'].map({True: 'rifamycin', False: ''})

InputCSV_NCBI['streptogramin'] = InputCSV_NCBI['AMR_genotypes'].str.contains(strgpattern)
InputCSV_NCBI['streptogramin'] = InputCSV_NCBI['streptogramin'].map({True: 'streptogramin', False: ''})

InputCSV_NCBI['streptothricin'] = InputCSV_NCBI['AMR_genotypes'].str.contains(strthrgpattern)
InputCSV_NCBI['streptothricin'] = InputCSV_NCBI['streptothricin'].map({True: 'streptothricin', False: ''})

InputCSV_NCBI['sulphonamide'] = InputCSV_NCBI['AMR_genotypes'].str.contains(sulpattern)
InputCSV_NCBI['sulphonamide'] = InputCSV_NCBI['sulphonamide'].map({True: 'sulphonamide', False: ''})

InputCSV_NCBI['tetracenomycin'] = InputCSV_NCBI['AMR_genotypes'].str.contains(tetmypattern)
InputCSV_NCBI['tetracenomycin'] = InputCSV_NCBI['tetracenomycin'].map({True: 'tetracenomycin', False: ''})

InputCSV_NCBI['tetracycline'] = InputCSV_NCBI['AMR_genotypes'].str.contains(tetpattern)
InputCSV_NCBI['tetracycline'] = InputCSV_NCBI['tetracycline'].map({True: 'tetracycline', False: ''})

InputCSV_NCBI['thiostrepton'] = InputCSV_NCBI['AMR_genotypes'].str.contains(thiopattern)
InputCSV_NCBI['thiostrepton'] = InputCSV_NCBI['thiostrepton'].map({True: 'thiostrepton', False: ''})

InputCSV_NCBI['trimethoprim'] = InputCSV_NCBI['AMR_genotypes'].str.contains(dfrpattern)
InputCSV_NCBI['trimethoprim'] = InputCSV_NCBI['trimethoprim'].map({True: 'trimethoprim', False: ''})

InputCSV_NCBI['tuberactinomycin'] = InputCSV_NCBI['AMR_genotypes'].str.contains(tubrpattern)
InputCSV_NCBI['tuberactinomycin'] = InputCSV_NCBI['tuberactinomycin'].map({True: 'tuberactinomycin', False: ''})

InputCSV_NCBI['AMR-efflux'] = InputCSV_NCBI['AMR_genotypes'].str.contains(AMRfluxpattern)
InputCSV_NCBI['AMR-efflux'] = InputCSV_NCBI['AMR-efflux'].map({True: 'AMR-efflux', False: ''})

InputCSV_NCBI['Biocide-efflux'] = InputCSV_NCBI['stress_genotypes'].str.contains(BCDfluxpattern)
InputCSV_NCBI['Biocide-efflux'] = InputCSV_NCBI['Biocide-efflux'].map({True: 'Biocide-efflux', False: ''})

InputCSV_NCBI['biocide'] = InputCSV_NCBI['stress_genotypes'].str.contains(biocidepattern)
InputCSV_NCBI['biocide'] = InputCSV_NCBI['biocide'].map({True: 'biocide', False: ''})

InputCSV_NCBI['Metal'] = InputCSV_NCBI['stress_genotypes'].str.contains(MTLpattern)
InputCSV_NCBI['Metal'] = InputCSV_NCBI['Metal'].map({True: 'Metal', False: ''})

#replace empty cells with NaN so can concatenate without worrying about extra commas
InputCSV_NCBI['aminoglycoside'].replace('', np.nan, inplace=True)
InputCSV_NCBI['betalactam'].replace('', np.nan, inplace=True)
InputCSV_NCBI['bleomycin'].replace('', np.nan, inplace=True)
InputCSV_NCBI['fosfomycin'].replace('', np.nan, inplace=True)
InputCSV_NCBI['fusidic acid'].replace('', np.nan, inplace=True)
InputCSV_NCBI['glycopeptide'].replace('', np.nan, inplace=True)
InputCSV_NCBI['MLS'].replace('', np.nan, inplace=True)
InputCSV_NCBI['macrolide'].replace('', np.nan, inplace=True)
InputCSV_NCBI['lincosamide'].replace('', np.nan, inplace=True)
InputCSV_NCBI['lincosamide_streptogramin'].replace('', np.nan, inplace=True)
InputCSV_NCBI['mupirocin'].replace('', np.nan, inplace=True)
InputCSV_NCBI['nitroimidazole'].replace('', np.nan, inplace=True)
InputCSV_NCBI['phenicol'].replace('', np.nan, inplace=True)
InputCSV_NCBI['phenicol_oxazolidinone'].replace('', np.nan, inplace=True)
InputCSV_NCBI['phenicol_quinolone'].replace('', np.nan, inplace=True)
InputCSV_NCBI['pluromutilin'].replace('', np.nan, inplace=True)
InputCSV_NCBI['polymyxin'].replace('', np.nan, inplace=True)
InputCSV_NCBI['quinolone'].replace('', np.nan, inplace=True)
InputCSV_NCBI['rifamycin'].replace('', np.nan, inplace=True)
InputCSV_NCBI['streptogramin'].replace('', np.nan, inplace=True)
InputCSV_NCBI['streptothricin'].replace('', np.nan, inplace=True)
InputCSV_NCBI['sulphonamide'].replace('', np.nan, inplace=True)
InputCSV_NCBI['tetracenomycin'].replace('', np.nan, inplace=True)
InputCSV_NCBI['tetracycline'].replace('', np.nan, inplace=True)
InputCSV_NCBI['thiostrepton'].replace('', np.nan, inplace=True)
InputCSV_NCBI['trimethoprim'].replace('', np.nan, inplace=True)
InputCSV_NCBI['tuberactinomycin'].replace('', np.nan, inplace=True)


#create a new column that concatenates all of the parsed antibiotic class information into one
#note that the biocide and metal categories are left out...
InputCSV_NCBI['Antibiotic_Class'] = InputCSV_NCBI[['aminoglycoside', 'betalactam','bleomycin', 'fosfomycin',
                                                   'fusidic acid','glycopeptide','MLS', 'macrolide', 'lincosamide',
                                                   'lincosamide_streptogramin','mupirocin','nitroimidazole','phenicol',
                                                   'phenicol_oxazolidinone','phenicol_quinolone','pluromutilin',
                                                   'polymyxin', 'quinolone','rifamycin','streptogramin',
                                                   'streptothricin','sulphonamide', 'tetracenomycin','tetracycline',
                         'thiostrepton','trimethoprim','tuberactinomycin']].apply(lambda x: ','.join(x[x.notnull()]), axis=1)

#remove all of the extra columns I made
InputCSV_NCBI = InputCSV_NCBI.drop(['aminoglycoside', 'betalactam','bleomycin', 'fosfomycin',
                                                   'fusidic acid','glycopeptide','MLS', 'macrolide', 'lincosamide',
                                                   'lincosamide_streptogramin','mupirocin','nitroimidazole','phenicol',
                                                   'phenicol_oxazolidinone','phenicol_quinolone','pluromutilin',
                                                   'polymyxin', 'quinolone','rifamycin','streptogramin',
                                                   'streptothricin','sulphonamide', 'tetracenomycin','tetracycline',
                         'thiostrepton','trimethoprim','tuberactinomycin'], axis=1)

#compare the IFSAC and Source2 columns. If both have text, only keep the IFSAC column.
#replace empty cells with NaN so can concatenate without worrying about extra commas
InputCSV_NCBI['Source_IFSAC'].replace('', np.nan, inplace=True)
InputCSV_NCBI['Source2'].replace('', np.nan, inplace=True)

#now, if there is an IFSAC category then paste that in the source column... otherwise, paste from source2 (curated by Ashley Cooper)
InputCSV_NCBI['Source'] = np.where(
    InputCSV_NCBI['Source_IFSAC'].isna(),
    InputCSV_NCBI['Source2'],
    InputCSV_NCBI['Source_IFSAC'],
)

#output a new csv file with source, AMR-class, biocide, and metal resistance data
InputCSV_NCBI.to_csv(args.outfile)
