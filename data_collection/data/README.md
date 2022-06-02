# Data Description

- `PPL (Prospective Program List)` : Manually aggregated list of Data programs offered at universities under country-wise rank of 50 in India and USA respectively. Rawest form of data
  - PPL_India.xlsx
  - PPL_USA.xlsx
- `intermediate` : Data obtained by scraping URLs of program webpages (where websites were available). If the program did not have a dedicated webpage, manual collection was employed.
  - program_description_india.csv
  - program_description_usa.csv
  - program_other_data_india.csv
  - program_other_data_usa.csv
- `processed` : Transformed data usable for analysis. Also includes .xlsx files that have raw data regarding course curriculums in the programs. This information has been manually collected from the webpages using inspection. *(If you wish to perform analysis on your own, these are the datasets you need)*
  - india_pgms.csv
  - india_curr.csv
  - usa_pgms.csv
  - usa_curr.csv
- `labelled` : A single dataset aggregating all the collected data together after labelling them in accordance with the theoretical framework used for this project
- `notebooks_for_cleaning` : Code used for data transformations
