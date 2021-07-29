import streamlit as st
import pandas as pd

def show():
    st.title("About the Dashboard")
    st.markdown("b")
    st.header("How to use the Dashboard?")
    st.markdown("n")
    st.header("What is ...")
    with st.beta_expander("Data Science Education?"):
        st.text("""
        ...
        """)
    with st.beta_expander("a Data Program?"):
        st.text("""
        ...
        """)

    

    st.sidebar.subheader("Links")
    st.sidebar.markdown("""
    - [Project Code]()
    """)