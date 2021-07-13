import os
import random

from preprocess import CourseNamesProcessor

import streamlit as st
import pandas as pd

LABELS = ""

def shuffle_data(df):
    return df.sample(frac=1)

def annotate(labels):
    labels_in_string = "; ".join(labels)
    # update labelled words
    st.session_state.labelled[st.session_state.current_word] = labels_in_string

    if len(st.session_state.words_to_label) != 0:
        st.session_state.words_to_label.remove(st.session_state.current_word)
        st.session_state.current_word = st.session_state.words_to_label[0]

def save_progress():
    for key, value in st.session_state.labelled.items():
        df.loc[df['word'] == key, 'labels'] = value
    df.to_csv("labelled_words.csv", index=False)
    st.sidebar.success("Words labelled in this session have been updated to the labelled words file")

def show():

    st.title("Greater Data Science Category Labeller")

    df = pd.read_csv("labelled_words.csv")
    df = shuffle_data(df)

    if "num_words_to_label" not in st.session_state:
        st.session_state.num_words_to_label =  df[df['labels'].isnull()].shape[0]

    if "words_to_label" not in st.session_state:
        st.session_state.words_to_label = list(df[df['labels'].isnull()]['word'])

    if "labelled" not in st.session_state:
        st.session_state.labelled = {}   # initially, no words are labelled
        st.session_state.current_word = st.session_state.words_to_label[0]

    st.sidebar.header("Information")
    st.sidebar.write(
        '''
        1. Multiple labels can be selected 
        2. If a label is ambiguous, assign it as "Not determinable"
        '''
    )
    st.sidebar.header("Save Progress")
    st.sidebar.write("Click the button below to store the data labelled so far as a .csv file")
    st.sidebar.button("Save into CSV", on_click=save_progress)

    st.header('Display Entries to Label')
    st.write("Add more labels please! - Softskills? Ethics? Not determined?")
    st.header('Labelling')

    col1, col2 = st.beta_columns(2)

    with col1:
        try:
            st.session_state["current_word"] = st.session_state.words_to_label[0]
        except:
            pass

        if len(st.session_state.words_to_label) != 0:
            form = st.form("label_form", clear_on_submit=True)
            labels = form.multiselect(
                "Choose Labels",
                [
                    "Data Gathering, Preparation and Exploration",
                    "Data Representation and Transformation",
                    "Computing with Data",
                    "Data Modeling",
                    "Data Visualization and Presentation",
                    "Science about Data Science",
                    "Not determinable",
                ],
                key="labels",
                help="Multiple labels can be chosen"
            )          

            submitted = form.form_submit_button("Submit")

            if submitted:
                labels_in_string = "; ".join(labels)
                st.session_state.labelled[st.session_state.current_word] = labels_in_string
                try:
                    st.session_state.words_to_label.remove(st.session_state.current_word)
                    st.session_state.current_word = st.session_state.words_to_label[0]
                except:
                    pass   
        else:
            st.success(
                f"Done!"
            )

    with col2:
        try:
            st.session_state["current_word"] = st.session_state.words_to_label[0]
            st.subheader(f"Word to label: {st.session_state.current_word}")
        except:
            pass

    st.subheader("Progress of Labelling")
    progress = st.progress(
        1 - round(len(st.session_state.words_to_label) / st.session_state.num_words_words_to_label, 2)
    )
    st.write(f"Number of words labelled in this session = {st.session_state.num_words_to_label - len(st.session_state.words_to_label)}")
    st.write(f"Number of words left to label = {len(st.session_state.words_to_label)}")

if __name__ == "__main__":
    show()