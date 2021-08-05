import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from pages.helpers import compute_score

st.session_state.program = None
st.session_state.country = None
st.session_state.comp_courses = None
st.session_state.scored = None

def show():

    st.header("Enter details of the program")
    with st.form("input_form"):
        cols = st.beta_columns([2,1])
        st.session_state.program = cols[0].text_input("Enter the name of the program",
            help="The full name of the program")
        st.session_state.country = cols[1].selectbox("country", ['India', 'USA', 'Another country'],
            help="The country in which the program is offered")
        st.session_state.comp_courses = st.text_input("Enter compulsory course titles, separate using commas",
            help="Use comma as separator")
        score_it = st.form_submit_button('Score Program')

    if score_it:
        st.session_state.scored = compute_score(st.session_state.program, st.session_state.comp_courses)
        st.session_state.scored = st.session_state.scored.T
        st.session_state.scored.columns = ['proportion']
        st.header(f"Report for Program")
        st.subheader(f"Name of program: {st.session_state.program}")
        st.subheader(f"Country: {st.session_state.country}")
        st.subheader("Proportion of each GDS Division")

        x = list(st.session_state.scored.index)
        y = st.session_state.scored['proportion']
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=x,
            y=y,
            marker_color="#125d98"
        ))
        fig.update_layout(
            title="Hover over plot for details",
            yaxis=dict(
                title="Proportion of program"
            )

        )
        st.plotly_chart(fig)

    '''
    st.sidebar.subheader("Links")
    st.sidebar.markdown("""
    - [Project Code]()
    """)
    '''