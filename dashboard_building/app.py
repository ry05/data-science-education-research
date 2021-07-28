import streamlit as st
import pandas as pd

from multipage_framework import MultiPage
from pages import home, explorer, scorer, find

app = MultiPage()
logo = "assets/app_header.png"
st.image(logo, width=800)

app.add_page("Explore Programs", explorer.show)
app.add_page("Home Page", home.show)
app.add_page("Score New Program", scorer.show)
app.add_page("Find Program", find.show)

app.run()