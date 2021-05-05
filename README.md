# source_and_resistance_categorizer
Using NCBI PathogenFinder Metadata tables (available at: https://www.ncbi.nlm.nih.gov/pathogens/)
this code categorizes and assigns:\
(1) isolation source and (2) antibiotic class, sanitizer and metal resistance

Isolation source data from NCBI has been curated for submissions up until 2021-04-20 for the following genera/species:

	Acinetobacter spp.	: 2021-04-20
	Aeromonas spp.		: 2021-04-21
	Campylobacter spp.	: 2021-04-20
	Citrobacter freundii	: 2021-04-20
	Clostridioides difficile: 2021-05-05
	Listeria spp.		: 2021-04-20
	Salmonella spp.		: 2021-04-20

This curated source data is in the provided "sources.csv" file.

The antimicrobial and metal resistance gene-data was obtained from the NCBI AMRFinderPlus database (available through the ftp at: https://www.ncbi.nlm.nih.gov/pathogens/).
