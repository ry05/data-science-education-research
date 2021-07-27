import streamlit as st
import pandas as pd

from multipage_framework import MultiPage
from pages import home, explorer, scorer

app = MultiPage()
st.title("GDS")

app.add_page("Explore Programs", explorer.show)
app.add_page("Home Page", home.show)
app.add_page("Score New Program", scorer.show)

app.run()