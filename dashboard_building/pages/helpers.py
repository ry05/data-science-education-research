"""
Helper functions
"""

import pandas as pd 

def load_data():
    pgm_data = pd.read_csv("../data/masters_data_programs_india_usa.csv")
    pgm_data = pgm_data[[
        "id",
        "uni_name",
        "pgm_name",
        "type",
        "country",
        "url",
        "subject",
        "dept_cat",
        "descr",
        "Data Gathering, Preparation and Exploration",
        "Data Representation and Transformation",
        "Computing woth Data",
        "Data Modeling",
        "Data Visualization and Presentation",
        "Science about Data Science",
        "gds_score",
    ]]
    gds_dictionary = pd.read_csv("../data/labelled_units_words.csv")

    return pgm_data, gds_dictionary