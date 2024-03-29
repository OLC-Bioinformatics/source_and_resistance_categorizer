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
The NIH/NCBI now provide IFSAC (Interagency Food Safety Analytics Collaboration - CDC) food categorization in the metadata files for select genera. (CDC website: https://www.cdc.gov/foodsafety/ifsac/projects/food-categorization-scheme.html). This categorization scheme was further simplified for use with this code/publication (see the sources_IFSAC.csv file).

Where IFSAC categories were not provided, isolation source for environmental/other (epi_type) data from NCBI has been curated* for submissions up until the listed dates for the following genera/species:

	Genus species		 Last Curation Date
	Acinetobacter spp.	: 2023-03-07
	Aeromonas spp.		: 2023-03-09
	Aeromonas salmonicida	: 2023-03-09
	Aeromonas sobria	: 2023-01-22
	Aeromonas veronii	: 2023-02-18
	Bacillus cereus		: 2023-03-13
	Campylobacter spp.	: 2023-03-11
	Citrobacter freundii	: 2023-03-13
	Clostridioides difficile: 2023-03-11
	Clostridium botulinum	: 2023-03-02
	Clostridium perfringens	: 2023-02-28
	Edwardsiella ictaluri	: 2023-02-24
	Edwardsiella piscicida	: 2023-02-02
	Edwardsiella tarda	: 2023-02-24
	Enterobacter spp.	: 2023-03-11
	Enterococcus faecalis	: 2023-03-13
	Enterococcus faecium	: 2023-03-13
	E. coli/Shigella	: 2023-03-11
	Klebsiella spp.		: 2023-03-13
	Klebsiella oxytoca	: 2023-03-11
	Listeria spp.		: 2023-03-13
	Listeria innocua	: 2023-03-10
	Pseudomonas aeruginosa	: 2023-03-12
	Pseudomonas putida	: 2023-02-23
	Salmonella spp.		: 2023-03-13
	Staphylococcus aureus	: 2023-03-13
	Vibrio cholerae		: 2023-03-08
	Vibrio harveyi		: 2023-03-08
	Vibrio parahaemolyticus	: 2023-03-09
	Vibrio vulnificus	: 2023-03-04

**The focus of this project was food and food products, so additional curation will be needed for other isolation sources (e.g. environment, farm, animal, food processing environments (slaughterhouse/processing), and wastewater sources).*

**Where categorization exist(s) for both IFSAC and the manually curated isolation source data, the IFSAC category is output as the priority by the script in the final 'Source' column**

## Usage:

Download and unpack source_and_resistance.py, sources_IFSAC.csv, sources.csv, and resistance_genes.csv files into desired folder.

This code searches through the NCBI metadata IFSAC_category, isolation_source, AMR_genotypes, and stress_genotypes columns, so if you are using your own custom csv file make sure the column headings in your file are isolation_source, AMR_genotypes, and stress_genotypes for columns containing the source, AMR genes, and biocide/metal resistance genes (respectively). Alternatively, you can just edit the python script.

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
                                   
	  -i INFILE    Input_Filename.csv
	  -o OUTFILE   Output_Filename.csv

\
The curated source data is in the provided "sources_IFSAC.csv" and "sources.csv" files.

The antimicrobial, biocide, and metal resistance gene-data was obtained from the NCBI AMRFinderPlus version 3.10 database and ReferenceGeneCatalog (available through the NCBI FTP at: https://www.ncbi.nlm.nih.gov/bioproject/PRJNA313047).

**AMRFinderPlus reference:**
Feldgarden, Michael, Vyacheslav Brover, Daniel H. Haft, Arjun B. Prasad, Douglas J. Slotta, Igor Tolstoy, Gregory H. Tyson et al. "Validating the AMRFinder tool and resistance gene database by using antimicrobial resistance genotype-phenotype correlations in a collection of isolates." Antimicrobial agents and chemotherapy 63, no. 11 (2019): e00483-19.

<br/>
<br/>

### Source Definitions
<br/>

**Animal -** any whole animal, biological tissue, or part of an animal including a wound sample from an animal. If a cut of meat was not specified, was placed in animal category. If a food animal and ‘carcass’ was listed, was considered meat. Mastitis milk, abceses,  and other diseased/infected parts from animals were left in animal category. Birds were also defined as animals.

**Animal environment -** environment(s) animals live in, excluding farm environments (farm, chicken house, cow paddock, chicken house fecal, etc) which were given their own category. ***this category requires additional curation/additions***

**Animal feces -** animal fecal samples, excluding farm fecal samples (eg. Chicken house fecal) which were categorized as 'farm'. ***this category requires additional curation/additions***

**Animal Feed -** Any feed or food listed as an animal or pet food, including domestic animal food, treats, silage, and livestock feed.

**Multi-product -** mixed food products or products that can’t be easily categorized: Chilli, if type was not specified and it could refer to prepared chilli or the pepper; Spreads and cream cheese mixtures; All salads (including tuna, egg, potato, and coleslaw) that may contain mixed ingredients; hummus; guacamole; salsa; ready to eat mixed products; sandwiches; fruitcake; sushi; pasta; sauces; etc.

**Food processing environment -** processing facilities, animal slaughterhouse environments, cutting boards, equipment. ***this category requires additional curation/additions***

**Plant -** any plant or part of a plant (not consumable, or not usually consumed) including leaves, roots. Plant environment was assumed to refer to "processing" plant environment, so was placed in the slaughterhouse/processing category. 

**Environment -** anything listed as environment without further clarification, and/or human restaurant and household environments. Also any outdoor environments, eg. yard, ground. ***this category requires additional curation/additions***

**Egg -** eggs and egg products, except for caviar which is categorized as Fish/Seafood.

**Feces -** anything listed as feces, stool, diarrhia, that does not also list a specific isolation area (e.g. farm feces are categorized as farm, bovine feces are categorized as feces). ***this category requires additional curation/additions***

**Fruit/Vegetables -** any fruit or vegetables, including frozen and ready to eat, and mixed fruit sources. French fries listed as food.

**Insect -** Any insect source, including fly traps from farms.

**Meat/Poultry -** meat and poultry products including raw and ready to eat products, sausages, hot dogs, snails, etc but excluding reptile meats and mixed products (like meat sauce, pates, and spreads)

**Nuts/Seeds -** nuts or seeds and nut products including nut butters. Does not include mixed products such as “sesame candy with pistachio”, which were labelled as multi-product.

**Fish/seafood -** Fish and seafood products, excluding mixed salads and mixed products which were categorized as foods.

**Water -** water sources including rivers, lake beds, ice water; but excluding aquarium, farm, and sewage sources. ***this category requires additional curation/additions***

**Farm -** All farm sources including crop fields, hatcheries, water from farm, irrigation water, farm manure, litter, and bedding. ***this category requires additional curation/additions***

**Herbs/Spices -** Dried herbs (e.g. dried parsley), red pepper flakes, cumin, powders, etc.

**Aquatic -** aquatic/sea creatures not always considered fish/seafood such as dolphins, coral, whales, and seals.
