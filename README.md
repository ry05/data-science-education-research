# Code Repository for "Analyzing the Content of Masters' Curricula using a Dictionary-based Approach"

Dissertation submitted in part completion of the MSc in Applied Social Data Science (2020-2021) at the Department of Methodology, London School of Economics and Political Science

## Project Abstract

The growing interest in data science has created a demand for well-trained professionals who can help organizations make better decisions with the help of data. As a response to this demand, data science education programs have been developed in universities across the world. These embryonic programs will greatly benefit from research that evaluates their contents to improve their effectiveness. However, there is a dearth of such research into the contents of these expensive programs and the ones that exist are mostly limited to a very small subset of the offered programs in the USA. In this project, I have made an attempt to study and evaluate these programs in a much broader sense and included programs from both India and the USA, making comparisons across the contents of data-related masters’ programs as well as administrative variables such as the funding of universities and types of departments offering the program. Data on 111 programs were collected and a dictionary approach was used to quantitatively analyze and compare the programs using the Greater Data Science framework. It was discovered that current programs place great focus in computing concepts while they do not offer enough focus on topics relating to reproducibility, ethics or other concepts that make a up a “science”. Differences were observed between programs across the two countries in the contents of the programs. A prototype of a web-based program recommender was developed to use the GDS dictionary created in this project to evaluate new programs. The dictionary approach was coupled with a content-based recommendation system to develop a program recommender that will connect learners to suitable programs. It is reasoned that this tool will be developed into a larger, more effective product in the future.
 
## Deployed Application

The `Data Program Selector` prototype developed can be viewed at [https://share.streamlit.io/ry05/data_program_selector_app/app.py](https://share.streamlit.io/ry05/data_program_selector_app/app.py)


## Repository Organization
------------

    ├── LICENSE                            
    ├── README.md                           
    ├── data_collection                     <- Overview and code involved in data collection
    |    ├── chromedriver_win32             <- Chromedriver installation for dynamic scraping
    |         ├── chromedriver.exe
    |    ├── data_collection                <- All about data collection methodology employed
    |         ├── README.md                 <- Explanantion of differesent data assets collected
    |         ├── PPL
    |         ├── intermediate
    |         ├── processed
    |         ├── labelled
    |         ├── notebooks_for_cleaning
    |    ├── scraping
    ├── data_analysis                       <- Code to analyse collected data
    |    ├── src                            <- Helper functions used
    |    ├── notebooks                      <- Jupyter notebooks and R markdown notebooks with data analysis
    |    ├── data_labeling                  <- Code for the data labelling software created in Streamlit
    ├── data_program_selector_development   <- Code for the Data PRogram Selector tool deployed on Streamlit
    ├── reports
    |   ├── Dissertation.pdf              <- Final copy of Dissertation submitted for degree 
    ├── .gitignore                        <- Files that need not be pushed to git
    ├── dse_logo.png                      <- PNG logo for project
    ├── requirements.txt                  <- The requirements file for reproducing the analysis environment.
    ├── setup.sh                          <- Bash script to install all dependencies for reproducing the project
--------
