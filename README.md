# source_and_resistance_categorizer
If used for publication, please cite:

Cooper *et al*., (INSERT ONCE PUBLISHED)


\
\
Using NCBI PathogenFinder Metadata tables (available at: https://www.ncbi.nlm.nih.gov/pathogens/),
this code categorizes and assigns:

(1) isolation source*

(2) antibiotic class, biocide and metal resistance

\
\
Isolation source for environmental/other (epi_type) data from NCBI has been curated* for submissions up until the listed dates for the following genera/species:

	Acinetobacter spp.	: 2021-04-20
	Aeromonas spp.		: 2021-04-21
	Campylobacter spp.	: 2021-04-20
	Citrobacter freundii	: 2021-04-20
	Clostridioides difficile: 2021-05-05
	Clostridium botulinum	: 2021-04-06
	Clostridium perfringens	: 2021-04-24
	Enterobacter spp.	: 2021-05-05
	Enterococcus faecalis	: 2021-04-20
	Enterococcus faecium	: 2021-04-20
	E. coli/Shigella	: 2021-04-20
	Klebsiella		: 2021-05-06
	Klebsiella oxytoca	: 2021-05-05
	Listeria spp.		: 2021-04-20
	Salmonella spp.		: 2021-04-20
	Staphylococcus aureus	: 2021-05-12
	Vibrio cholerae		: 2021-04-22
	Vibrio parahaemolyticus	: 2021-05-05
	Vibrio vulnificus	: 2021-04-22

**The focus of this project was food and food products, so additional curation will be needed for other isolation sources (e.g. environment, farm, animal, slaughterhouse/processing, and wastewater sources).*


## Usage:

Download and unpack source_and_resistance.py, sources.csv, and resistance_genes.csv files into desired folder.

This code searches through the NCBI metadata isolation_source, AMR_genotypes, and stress_genotypes columns, so if using your own csv file make sure the column headings in your file are isolation_source, AMR_genotypes, and stress_genotypes for columns containing the source, AMR genes, and biocide/metal resistance genes (respectively). Alternatively, you can just edit the python script.

\
From command line:

	python source_and_resistance.py -i input.csv -o desired_output_name.csv
	

\
\
Help message
	
	usage: use "source_and_resistance.py --help" for more information
	
	details
	
	optional arguments:
	  -h, --help   show this help message and exit
	  --info INFO  
                                   NCBI Source and Resistance Assignment
                                   Please cite "Cooper et al., INSERT CITATION"
                                   
                                   Input and output should be in csv format
                                   If using metadata files from NCBI PathogenFinder FTP, do not forget to remove the "#" in the first line
                                   The "resistance_genes.csv" and "sources.csv" files must be in the same directory as this python script
                                   Source database last updated: 2021-04-20 (see README for more details)
                                   
	  -i INFILE    Input Filename.csv
	  -o OUTFILE   Output Filename.csv

\
The curated source data is in the provided "sources.csv" file.

The antimicrobial, biocide, and metal resistance gene-data was obtained from the NCBI AMRFinderPlus version 3.10 database and ReferenceGeneCatalog (available through the NCBI FTP at: https://www.ncbi.nlm.nih.gov/bioproject/PRJNA313047).

AMRFinderPlus reference:
Feldgarden, Michael, Vyacheslav Brover, Daniel H. Haft, Arjun B. Prasad, Douglas J. Slotta, Igor Tolstoy, Gregory H. Tyson et al. "Validating the AMRFinder tool and resistance gene database by using antimicrobial resistance genotype-phenotype correlations in a collection of isolates." Antimicrobial agents and chemotherapy 63, no. 11 (2019): e00483-19.

<br/>
<br/>

### Source Definitions
<br/>

**Animal -** any whole animal, biological tissue, or part of an animal including a wound sample from an animal. If a cut of meat was not specified, was placed in animal category. If a food animal and ‘carcass’ was listed, was considered meat. Mastitis milk, abceses,  and other diseased/infected parts from animals were left in animal category. Birds were also defined as animals.

**Animal environment -** environment(s) animals live in, excluding farm environments (farm, chicken house, cow paddock, chicken house fecal, etc) which were given their own category. ***this category requires additional curation/additions***

**Animal feces -** animal fecal samples, excluding farm fecal samples (eg. Chicken house fecal) which were categorized as 'farm'. ***this category requires additional curation/additions***

**Food -** mixed food products or products that can’t be easily categorized: Chilli, if type was not specified and it could refer to prepared chilli or the pepper; Spreads and cream cheese mixtures; All salads (including tuna, egg, potato, and coleslaw) that may contain mixed ingredients; hummus; guacamole; salsa; ready to eat mixed products; sandwiches; fruitcake; sushi; pasta; sauces; etc.

**Slaughterhouse/processing -** processing facilities, animal slaughterhouse environments, cutting boards, equipment. ***this category requires additional curation/additions***

**Plant -** any plant or part of a plant (not consumable, or not usually consumed) including leaves, roots. Plant environment was assumed to refer to "processing" plant environment, so was placed in the slaughterhouse/processing category. 

**Environment -** anything listed as environment without further clarification, and/or human restaurant and household environments. Also any outdoor environments, eg. yard, ground. ***this category requires additional curation/additions***

**Feces -** anything listed as feces, stool, diarrhia, that does not also list a specific isolation area (e.g. farm feces are categorized as farm, bovine feces are categorized as feces). ***this category requires additional curation/additions***

**Feed -** Any feed or food listed as an animal or pet food, including domestic animal food, treats, silage, and livestock feed.

**Fruit/vegetable -** any fruit or vegetables, including frozen and ready to eat, and mixed fruit sources. French fries listed as food.

**Insect -** Any insect source, including fly traps from farms.

**Meat -** meat products including raw and ready to eat products, sausages, hot dogs, snails, etc but excluding reptile meats and mixed products (like meat sauce, pates, and spreads)

**Nuts -** nuts and nut products including nut butters. Does not include mixed products such as “sesame candy with pistachio”, which were labelled as foods.

**Fish/seafood -** Fish and seafood products, excluding mixed salads and mixed products which were categorized as foods.

**Water -** water sources including rivers, lake beds, ice water; but excluding aquarium, farm, and sewage sources. ***this category requires additional curation/additions***

**Farm -** All farm sources including crop fields, hatcheries, water from farm, irrigation water, farm manure, litter, and bedding. ***this category requires additional curation/additions***

**Spices/herbs -** Dried herbs (e.g. dried parsley), red pepper flakes, cumin, powders, etc.

**Aquatic -** aquatic/sea creatures not always considered fish/seafood such as dolphins, coral, whales, and seals.
