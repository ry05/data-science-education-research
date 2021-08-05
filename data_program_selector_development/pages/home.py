import streamlit as st

def show():
    st.header("About the Tool")
    st.markdown("""
    The tool was built to help prospective graduate learners find suitable data programs in India and the USA.
   
    
    """)
    st.header("How to use the Dashboard?")
    st.markdown("""
    1. Select the desired page using the dropdown in the control panel
    2. Follow the instructions on the selected page

    """)
    st.header("What is ...")
    with st.beta_expander("Data Science Education?"):
        st.text("""
        In the context of the author's research, 'Data Science Education' is defined as collective set of practices involved in disseminating knowledge about
        data science concepts involving, but not limited to the creation of training programs (both academic as well as non-academic),
        the efforts of marketing these programs to a suitable market and the implementation of the programs to cultivate a responsible generation of data-driven thinkers
        """)
    with st.beta_expander("A Data Program?"):
        st.text("""
        In the context of the author's research, a 'data program' is a graduate program with one of the keywords;
        data, analytics, analysis, artificial intelligence, ai, machine learning or ml in the title of the program
        """)

    '''
    st.sidebar.subheader("Links")
    st.sidebar.markdown("""
    - [Project Code]()
    """)
    '''