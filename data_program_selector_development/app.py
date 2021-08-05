import streamlit as st
import pandas as pd
from PIL import Image
from multipage_framework import MultiPage
from pages import home, scorer, find

logo = Image.open('assets/dse_logo.png')
st.set_page_config(
    page_title="Project Demo",
    page_icon=logo
)

@st.cache(allow_output_mutation=True)
def load_data():
    pgm_data = pd.read_csv("data\masters_data_programs_india_usa.csv")
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
        "Computing with Data",
        "Data Modeling",
        "Data Visualization and Presentation",
        "Science about Data Science",
        "gds_score",
    ]]
    gds_dictionary = pd.read_csv("data/labelled_units_words.csv")

    return pgm_data, gds_dictionary

# create session state variables
st.session_state.df, st.session_state.gds_dictionary = load_data()


# instantiate a MultiPage app object
app = MultiPage()
logo = "assets/app_header.png"
st.image(logo, width=800)

app.add_page("Home Page", home.show)
app.add_page("Score New Program", scorer.show)
app.add_page("Find Program", find.show)

app.run()