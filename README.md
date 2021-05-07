# source_and_resistance_categorizer
Using NCBI PathogenFinder Metadata tables (available at: https://www.ncbi.nlm.nih.gov/pathogens/),
this code categorizes and assigns:

(1) isolation source

(2) antibiotic class, biocide and metal resistance

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
	Vibrio cholerae		: 2021-04-22
	Vibrio parahaemolyticus	: 2021-05-05
	Vibrio vulnificus	: 2021-04-22

*The focus of this project was food and food products, so additional curation may be required/needed for other isolation sources (eg. environment, farm, animal, and wastewater sources).

Usage:

Download and unpack python code, sources.csv, and resistance_genes.csv files into folder.

	python source_and_resistance.py -i input.csv -o desired_output_name.csv
	

This curated source data is in the provided "sources.csv" file.

The antimicrobial and metal resistance gene-data was obtained from the NCBI AMRFinderPlus database (available through the ftp at: https://www.ncbi.nlm.nih.gov/pathogens/).
