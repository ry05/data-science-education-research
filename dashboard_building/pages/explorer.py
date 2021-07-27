import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

df = pd.read_csv("../data_collection/data/labelled/masters_data_programs_india_usa.csv")

def show():

    st.header("Dashboard")
    st.header("[Logo here]")

    st.subheader("Data preview")
    st.write(df.head())

    fig = make_subplots(
        rows=3, cols=2,
        specs=[[{}, {}],
               [{"colspan": 2}, None],
               [{"colspan": 2}, None]],
        print_grid=True,
        subplot_titles=("First Subplot","Second Subplot", "Third Subplot", "Fourth Subplot"))
    
    x = list(df.country.value_counts().index)
    y = df.country.value_counts()
    fig.add_trace(go.Bar(x=x, y=y),
              row=1, col=1)

    x = list(df.type.value_counts().index)
    y = df.type.value_counts()
    fig.add_trace(go.Bar(x=x, y=y),
              row=1, col=2)

    x = list(df.subject.value_counts().index)
    y = df.subject.value_counts()
    fig.add_trace(go.Bar(x=x, y=y),
              row=2, col=1)

    x = list(df.dept_cat.value_counts().index)
    y = df.dept_cat.value_counts()
    fig.add_trace(go.Bar(x=x, y=y),
              row=3, col=1)

    fig.update_layout(height=1000, width=900, showlegend=False)
    st.plotly_chart(fig)

    st.subheader("GDS Scores Exploration")

    fig = px.scatter(
        df,
        x="Data Gathering, Preparation and Exploration",
        y="Data Representation and Transformation",
        size="gds_score", color="country", hover_name="id"
    )
    fig.update_layout(height=600, width=900, showlegend=False)
    st.plotly_chart(fig)

    df_score_sort = df.sort_values(by='gds_score', ascending=False)
    programs = list(df_score_sort.id)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_score_sort.gds_score.values,
        y=programs,
        marker=dict(color="crimson", size=12),
        mode="markers",
        name="GDS Score",
    ))
    fig.update_layout(height=1500, width=1000, showlegend=False)
    st.plotly_chart(fig)
    








    st.sidebar.subheader("Links")
    st.sidebar.markdown("""
    - [Project Guide]()
    - [Project Code]()
    """)