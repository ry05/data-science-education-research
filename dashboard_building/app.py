import streamlit as st
import pandas as pd

def show(df):

    st.title("Dashboard")
    st.header("[Logo here]")
    st.sidebar.header("Control Panel")
    option = st.sidebar.selectbox("Select Task", ['View results of project', 'Score a new program'])
    st.write(df.head())
    st.write(df.describe())

if __name__ == "__main__":
    PGM_DATA = pd.read_csv("../data_collection/data/labelled/masters_data_programs_india_usa.csv")
    show(PGM_DATA)