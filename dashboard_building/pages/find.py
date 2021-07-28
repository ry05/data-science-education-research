import streamlit as st
import pandas as pd

def show():
    st.header("How to find a 'suitable' data program?")
    st.markdown("text")

    with st.form(key="basic_filters"):
        st.subheader("Basic Filters")
        cols1 = st.beta_columns(2)
        cols1[0].multiselect("Select country", ["India", "USA"], help="Can select more than one country")
        cols1[1].multiselect("Select type of university based on funding",
            ["Private", "Public"], help="Can select more than one funding status")
        cols2 = st.beta_columns(2)
        cols2[0].multiselect("Select subject",
            ["Data science", "Aritificial Intelligence", "Business Analytics", "Analytics"],
            help="Which subject(s) do you want to learn?")
        cols2[1].multiselect("Select department",
            ["Data-related", "Engineering-related", "Management-related"],
            help="Which kind of department would you prefer?")
        apply_basic = st.form_submit_button("Apply basic filters")

    st.text("Print number of programs qualifying after basic filters. If none, print a message")

    with st.form(key="advanced_filters"):
        st.subheader("Advanced filters")
        cols = st.beta_columns(2)
        cols[0].markdown("""
        GDS Divisions and corresponding ids are  
        GDS 1 - 1  
        GDS 2 - 2  
        GDS 3 - 3  
        GDS 4 - 4  
        GDS 5 - 5  
        GDS 6 - 6  
        """)
        cols[1].text_input("Arrange GDS divisions by index based on order of preference (highest to lowest)",
            help="Use comma as separator")
        apply_advanced = st.form_submit_button("Apply advanced filters")
    
    with st.form(key="get_similar"):
        st.subheader("Get similar programs")
        st.multiselect("Select country", ["India", "USA"], help="Which country(ies) do you want to study in?")
        get_sim = st.form_submit_button("Get similar programs")
        st.text("Top 5 programs in tabular format")

        
        




    st.sidebar.subheader("Links")
    st.sidebar.markdown("""
    - [Project Code]()
    """)