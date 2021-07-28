import streamlit as st
import pandas as pd

def show():
    st.header("How does scoring work?")
    st.markdown("text")

    st.header("Enter details of the program")
    with st.form("input_form"):
        cols = st.beta_columns([2,1])
        cols[0].text_input("Enter the name of the program",
            help="The full name of the program")
        cols[1].selectbox("country", ['India', 'USA', 'Another country'],
            help="The country in which the program is offered")
        st.text_input("Enter compulsory course titles, one per line",
            help="One per line is mandatory for the program to work")
        score_it = st.form_submit_button('Score Program')
    
    st.header(f"Report for program")




    

    st.sidebar.subheader("Links")
    st.sidebar.markdown("""
    - [Project Code]()
    """)