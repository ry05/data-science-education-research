import streamlit as st
import pandas as pd

from pages.helpers import rank_programs

def show():
    st.header("How to find a 'suitable' data program?")
    st.markdown("text")

    with st.form(key="basic_filters"):
        st.subheader("Basic Filters")
        cols1 = st.beta_columns(2)
        countries = cols1[0].multiselect("Select country", ["India", "USA"], help="Can select more than one country")
        types = cols1[1].multiselect("Select type of university based on funding",
            ["Private", "Public"], help="Can select more than one funding status")
        cols2 = st.beta_columns(2)
        subjects = cols2[0].multiselect("Select subject",
            ["Data Science", "Aritificial Intelligence", "Business Analytics", "Analytics"],
            help="Which subject(s) do you want to learn?")
        depts = cols2[1].multiselect("Select department",
            ["Data-related", "Engineering-related", "Management-related"],
            help="Which kind of department would you prefer?")
        apply_basic = st.form_submit_button("Apply basic filters")

    if apply_basic:
        # update session variables
        st.session_state.countries = countries
        st.session_state.types = types
        st.session_state.subjects = subjects
        st.session_state.depts = depts

        # filter programs
        st.session_state.filtered = st.session_state.df[
            (st.session_state.df.country.isin(st.session_state.countries)) &
            (st.session_state.df.type.isin(types)) &
            (st.session_state.df.subject.isin(subjects)) &
            (st.session_state.df.dept_cat.isin(depts))
        ]

        if st.session_state.filtered.shape[0] != 0:
            st.write(st.session_state.filtered[['uni_name', 'pgm_name', 'url']])
        else:
            st.write("No programs in the database with these filters")

    with st.form(key="advanced_filters"):
        st.subheader("Advanced filters")
        cols = st.beta_columns(2)
        cols[0].markdown("""
        GDS Divisions and corresponding ids are  
        GDS 1 - Data Gathering, Preparation and Exploration  
        GDS 2 - Data Representation and Transformation  
        GDS 3 - Computing with Data  
        GDS 4 - Data Modeling  
        GDS 5 - Data Visualization and Presentation  
        GDS 6 - Science about Data Science  
        """)
        priority = cols[1].text_input("Arrange GDS divisions by index based on order of preference (highest to lowest)",
            help="Use comma as separator")
        apply_advanced = st.form_submit_button("Apply advanced filters")

        if apply_advanced:
            st.session_state.weighted = rank_programs(st.session_state.filtered, priority)
            st.write(st.session_state.weighted.head())
    
    with st.form(key="get_similar"):
        st.subheader("Get similar programs")
        st.multiselect("Select country", ["India", "USA"], help="Which country(ies) do you want to study in?")
        get_sim = st.form_submit_button("Get similar programs")
        st.text("Top 5 programs in tabular format")

        
        




    st.sidebar.subheader("Links")
    st.sidebar.markdown("""
    - [Project Code]()
    """)