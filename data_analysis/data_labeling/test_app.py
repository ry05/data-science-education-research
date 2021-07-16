import random

import streamlit as st
import pandas as pd

from preprocess import TextPreprocessor

COMPULSORY_COURSES_INDIA_PATH = "../../data_collection/data/processed/india_curr.csv"
COMPULSORY_COURSES_USA_PATH = "../../data_collection/data/processed/usa_curr.csv"

def load_compulsory_courses():
    compulsory_courses_india = pd.read_csv(COMPULSORY_COURSES_INDIA_PATH)
    compulsory_courses_usa = pd.read_csv(COMPULSORY_COURSES_USA_PATH)
    compulsory_courses_usa.drop(['Unnamed: 4', 'Unnamed: 5'], inplace=True, axis=1)

    compulsory_courses = pd.concat([compulsory_courses_india, compulsory_courses_usa])
    compulsory_courses = compulsory_courses.sample(frac=1)
    compulsory_courses = compulsory_courses.reset_index(drop=True)

    compulsory_courses.fillna('', inplace=True)

    return compulsory_courses

def process_course_names(compulsory_courses):

    compulsory_courses['course_name_processed'] = compulsory_courses['compulsory course'].\
        apply(lambda x: TextPreprocessor(x).preprocess_text())
    
    return compulsory_courses

def make_words_to_label_list(compulsory_courses):

    all_words = " ".join(compulsory_courses['course_name_processed']).split()
    unique_words = list(set(all_words))
    random.shuffle(unique_words)

    return unique_words

def get_courses_with_the_word(compulsory_courses, word):

    courses_with_the_word = compulsory_courses[
        compulsory_courses['course_name_processed'].apply(lambda x: word in x.split())
    ]
    courses_with_the_word = courses_with_the_word.reset_index(drop=True)
    
    return courses_with_the_word

def show():

    st.title("Word Labeller for GDS Classification")
    st.write("A graphical interface to label each unique word occuring in course titles into one of the 6 possible categories")
    with st.beta_expander("What is GDS?"):
        st.write("""
            Greater Data Science(GDS) is a framework devised by David Donoho in the 2017 paper, "50 Years of Data Science".
            It is the theoretical basis for this research project of Data Science Education.
            GDS identifies 6 key activities that inform the full scope of Data Science. These are
            - Data Gathering, Preparation and Exploration
            - Data Representation and Transformation
            - Computing with Data
            - Data Modeling
            - Data Visualization and Presentation
            - Science about Data Science        
        """)

    with st.beta_expander("How does this work?"):
        st.write("""
            1. All titles of compulsory courses across the programs under study are broken to form words
            2. The unique words are displayed here one after the other
            3. Along with a word, the courses' titles and descriptions are also displayed for those courses' who contain the displayed word in their titles
            4. The researcher inspects the displayed data related to the word and labels the word into one or more GDS categories    
        """)

    with st.beta_expander("How does the researcher label each word?"):
        st.write("""
            **All labelling is performed by the researcher after consulting the list of possible concepts under each
            GDS division as per Donoho.**  

            1. First, inspect the word itself. If the word is ambiguous (like 'principles'), then consult the details of the courses displayed with the word  
            2. If there is more than one course that contains this word in the title, then place the word into GDS categories that are identified as existent across all these courses  
            3. If even the perusal of courses don't help label the word, label it based on the word itself, provided the word is not ambiguous  
            4. Even if a word seems to fit point 2 well, if the word itself is ambiguous or unrelated to data science as such, the word is to be labelled as "Not determinable"  
        """)

    with st.beta_expander("Why label individual words?"):
        st.write("""
            This is an attempt to create a GDS dictionary for GDS research. Hence the labelling of words.
            This method is not promised to be the the most robust. Yet, it is a good starting point and a better
            alternative than labelling each course (which was the first approach).
        """)

    # get compulsory courses for display
    comp_courses_df = load_compulsory_courses()
    comp_courses_df = process_course_names(comp_courses_df)

    try:
        st.session_state.labelled_df = pd.read_csv("labelled_units_words.csv")
        completed_words = list(st.session_state.labelled_df.words)
        words = [word for word in make_words_to_label_list(comp_courses_df) if word not in completed_words]
    except FileNotFoundError:
        words = make_words_to_label_list(comp_courses_df)

    if "num_words_to_label" not in st.session_state:
        st.session_state.num_words_to_label =  len(words)

    if "words_to_label" not in st.session_state:
        st.session_state.words_to_label = words

    if "labelled" not in st.session_state:
        st.session_state.labelled = {}
        st.session_state.current_word = st.session_state.words_to_label[0]

    def save_progress():

        if "labelled_df" in st.session_state:
            temp_df = pd.DataFrame(dict(
                words = st.session_state.labelled.keys(),
                labels = st.session_state.labelled.values(),
            ))
            st.session_state.labelled_df = pd.concat([st.session_state.labelled_df, temp_df])
            st.session_state.labelled_df.to_csv("labelled_units_words.csv", index=False)
            st.sidebar.success("Words labelled in this session have been updated to the labelled words file")
        else:
            df = pd.DataFrame(dict(
                words = st.session_state.labelled.keys(),
                labels = st.session_state.labelled.values(),
            ))
            df.to_csv("labelled_units_words.csv", index=False)
            st.sidebar.success("Words labelled in this session have been updated to the labelled words file")

    st.sidebar.title("Action Center")
      
    if len(st.session_state.words_to_label) != 0:
        form = st.sidebar.form("label_form", clear_on_submit=True)
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

    st.subheader(f"Word to label: {st.session_state.current_word}")
    st.subheader("Compulsory courses with this word in the title")
    st.session_state.courses_with_current_word = get_courses_with_the_word(
        comp_courses_df, st.session_state.current_word
    )
    for i in range(st.session_state.courses_with_current_word.shape[0]):
        st.write(st.session_state.courses_with_current_word.loc[i, "compulsory course"])
        st.write(st.session_state.courses_with_current_word.loc[i, "course outcome or overview"])
        st.write(st.session_state.courses_with_current_word.loc[i, "topics covered"])
        st.write("---")    

    st.sidebar.subheader("Progress of Labeling")
    st.sidebar.progress(
        1 - round(len(st.session_state.words_to_label) / st.session_state.num_words_to_label, 2)
    )
    st.sidebar.write(f"Words labelled in this session = {st.session_state.num_words_to_label - len(st.session_state.words_to_label)}")
    st.sidebar.write(f"Words left to label = {len(st.session_state.words_to_label)}")

    st.sidebar.header("Save Progress")
    st.sidebar.write("Click the button below to store the data labelled so far as a .csv file")
    st.sidebar.button("Save into CSV", on_click=save_progress)

if __name__ == "__main__":
    show()