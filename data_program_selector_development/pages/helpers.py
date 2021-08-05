"""
Helper functions
"""

from collections import Counter
import statistics
import string
import re

import pandas as pd 
import numpy as np
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
nlp = spacy.load("en_core_web_md")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

LABELS = [
    "Data Gathering, Preparation and Exploration",
    "Data Representation and Transformation",
    "Computing with Data",
    "Data Modeling",
    "Data Visualization and Presentation",
    "Science about Data Science",
    "Not determinable",
]

class TextPreprocessor:

    def __init__(self, text):
        self.text = text

    def make_lowercase(self):
        self.text = self.text.lower()

    def remove_numbers(self):
        self.text = self.text.translate({ord(k): None for k in string.digits})

    def remove_unnecessary_whitespace(self):
        self.text = self.text.replace('\t', '').replace('\n', '')
        self.text = re.sub(' +', ' ', self.text)
        self.text = self.text.strip()

    def remove_urls(self):
        self.text = re.sub(r'http\S+', '', self.text)

    def remove_punctuations(self):
        self.text = self.text.translate({ord(k): None for k in string.punctuation})

    def remove_unicode_chars(self):
        self.text = self.text.encode('ascii', 'ignore').decode('utf-8')

    def remove_stopwords(self):
        without_stopwords = [word for word in self.text.split() if word not in STOP_WORDS]
        self.text = " ".join(without_stopwords)

    def preprocess_text(self):

        self.make_lowercase()
        self.remove_stopwords()
        self.remove_numbers()
        self.remove_punctuations()
        self.remove_urls()
        self.remove_unicode_chars()
        self.remove_unnecessary_whitespace()

        return self.text

class CourseNamesProcessor:

    def __init__(self, course_list):
        self.courses = course_list

    def remove_duplicates(self):
        self.courses =  list(set(self.courses))

    def remove_punctuations(self, course):
        return course.translate({ord(k): None for k in string.punctuation})

    def remove_numbers(self, course):
        return course.translate({ord(k): None for k in string.digits})

    def preprocess_course_names(self):
        self.courses = [course_name.lower().strip() for course_name in self.courses if len(course_name)!=0]
        self.courses = [self.remove_numbers(course_name) for course_name in self.courses]
        self.courses = [self.remove_punctuations(course_name) for course_name in self.courses]

    def remove_stopwords_in_course_names(self):
        stopword_free_courses = []
        temp = " <COURSE SEPARATOR> ".join(self.courses)
        for word in temp.split():
            if not(word in STOP_WORDS):
                stopword_free_courses.append(word)

        self.courses = " ".join(stopword_free_courses).split(" <COURSE SEPARATOR> ")

    def process_course_names(self):

        self.remove_duplicates()
        self.preprocess_course_names()
        self.remove_stopwords_in_course_names()
        self.remove_duplicates()

    def get_courses(self):

        self.process_course_names()

        return (self.courses)

class CourseScorer:
    """
    Scores each compulsory course in a dataframe of courses
    by assigning '1' to a GDS label if it is covered by the
    course
    """

    def __init__(self, labelled_dictionary, compulsory_course_data):

        self.dictionary = labelled_dictionary
        self.data = compulsory_course_data
        self.labels = LABELS

    def __str__(self):

        print("Overview of GDS classifier object")
        print(f"Number of labelled words in dictionary: {len(self.dictionary)}")
        print(f"Number of non-missing compulsory courses in data file: {self.data[self.data.notnull()].shape[0]}")
   
    def get_gds_labels_for_course(self, course_name):
        """Get the GDS labels for a course

        Args:
            course_name ([type]): [description]

        Returns:
            [type]: [description]
        """

        labels = ""

        if course_name == 'Not inferred':
            return course_name
        course_name_lower = course_name.lower()
        for word, label in zip(
            list(self.dictionary['words']), list(self.dictionary['labels'])):
            if word in course_name_lower:
                labels = labels + ";" + label

        return labels

    def convert_gds_labels_string_to_list(self, gds_labels_as_string):
        """Convert the GDS labels string representation into a list

        Args:
            gds_labels_as_string ([type]): [description]

        Returns:
            [type]: [description]
        """

        temp = gds_labels_as_string.split(";")
        temp = [element.strip() for element in temp if len(element) != 0]
        gds_labels = list(set(temp))

        if len(gds_labels) != 0:
            if 'Not determinable' in gds_labels:
                gds_labels.remove('Not determinable')

        return gds_labels

    def confirm_gds_labels_existence(self, gds_labels_as_string):
        """Confirm whether a particular GDS label exists or not

        Args:
            gds_labels_as_string ([type]): [description]

        Returns:
            [type]: [description]
        """

        x = self.convert_gds_labels_string_to_list(gds_labels_as_string)
        
        gds_labels_confirmed_dict = Counter(x)

        return gds_labels_confirmed_dict

    def get_status_label_existence(self, gds_labels_confirmed_dict, label):
        """Split a GDS label dictionary into separate features

        Args:
            gds_labels_confirmed_dict ([type]): [description]
            label ([type]): [description]

        Returns:
            [type]: [description]
        """
        try:
            p = gds_labels_confirmed_dict[label]
        except:
            p = 0

        return p
    
    def clean_up_data(self):

        self.data = self.data.drop([
            'course_name_processed',
            'gds_labels',
            'gds_label_dict'], axis=1)

        # remove programs with no info on compulsory courses
        self.data = self.data[self.data['compulsory course'] != 'Not inferred']

    def label_by_subject(self, x, subject):

        if subject in x.lower():
            return 1
        return 0

    def explicit_labelling(self):

        # data science
        self.data['Data Gathering, Preparation and Exploration'] = self.data['Data Gathering, Preparation and Exploration'] | self.data['compulsory course'].apply(lambda x: self.label_by_subject(x, "data science"))
        self.data['Data Representation and Transformation'] = self.data['Data Representation and Transformation'] | self.data['compulsory course'].apply(lambda x: self.label_by_subject(x, "data science"))
        self.data['Computing with Data'] = self.data['Computing with Data'] | self.data['compulsory course'].apply(lambda x: self.label_by_subject(x, "data science"))
        self.data['Data Modeling'] = self.data['Data Modeling'] | self.data['compulsory course'].apply(lambda x: self.label_by_subject(x, "data science"))
        self.data['Data Visualization and Presentation'] = self.data['Data Visualization and Presentation'] | self.data['compulsory course'].apply(lambda x: self.label_by_subject(x, "data science"))

        # artificial intelligence
        self.data['Data Gathering, Preparation and Exploration'] = self.data['Data Gathering, Preparation and Exploration'] | self.data['compulsory course'].apply(lambda x: self.label_by_subject(x, "artificial intelligence"))
        self.data['Data Representation and Transformation'] = self.data['Data Representation and Transformation'] | self.data['compulsory course'].apply(lambda x: self.label_by_subject(x, "artificial intelligence"))
        self.data['Computing with Data'] = self.data['Computing with Data'] | self.data['compulsory course'].apply(lambda x: self.label_by_subject(x, "artificial intelligence"))
        self.data['Data Modeling'] = self.data['Data Modeling'] | self.data['compulsory course'].apply(lambda x: self.label_by_subject(x, "artificial intelligence"))

    def score_courses_by_gds(self):

        self.data["course_name_processed"] = self.data['compulsory course'].\
            apply(lambda x: TextPreprocessor(x).preprocess_text())
        self.data['gds_labels'] = self.data['course_name_processed'].apply(lambda x: self.get_gds_labels_for_course(x))
        self.data['gds_label_dict'] = self.data['gds_labels'].apply(self.confirm_gds_labels_existence)

        for label in self.labels:
            self.data[label] = None

        for label in self.labels:
            self.data[label] = self.data.gds_label_dict.apply(lambda x: self.get_status_label_existence(x, label))

        self.explicit_labelling()
        self.clean_up_data()

        return self.data
        

class ProgramScorer:

    def __init__(self, labelled_dictionary, compulsory_course_data):

        course_scorer = CourseScorer(labelled_dictionary, compulsory_course_data)
        self.scored_course_data = course_scorer.score_courses_by_gds()

    def group_courses_by_url(self):

        self.scored_program_data = self.scored_course_data.\
            groupby(['url'], as_index=False).\
                agg({
                    'Data Gathering, Preparation and Exploration': 'sum',
                    'Data Representation and Transformation': 'sum',
                    'Computing with Data': 'sum',
                    'Data Modeling': 'sum',
                    'Data Visualization and Presentation': 'sum',
                    'Science about Data Science': 'sum',
                    'Not determinable': 'sum',
                })

    def score_programs_by_gds(self):

        self.group_courses_by_url()
        return self.scored_program_data


class ScoreNormalizer:

    def __init__(self, scored_df):

        self.scored_df = scored_df
        self.labels = LABELS

    def normalize(self):

        normalized_scores = self.scored_df[self.labels].\
            div(self.scored_df[self.labels].sum(axis=1), axis=0)

        return normalized_scores

    def update_scored_df(self):

        normalized_scores = self.normalize()
        self.scored_df = self.scored_df.drop(self.labels, axis=1)
        self.scored_df = pd.concat([self.scored_df, normalized_scores], axis=1)

        return self.scored_df

class GDSBandAllocator:

    def __init__(self, scored_df):

        self.scored_df = scored_df
        self.labels = LABELS

    def compute_gds_stdev(self):

        temp = self.scored_df[[
            "Data Gathering, Preparation and Exploration",
            "Data Representation and Transformation",
            "Computing with Data",
            "Data Modeling",
            "Data Visualization and Presentation",
            "Science about Data Science",
        ]]

        gds_stdev = temp.apply(lambda x: statistics.stdev(x), axis=1)

        self.scored_df['gds_score'] = gds_stdev

    def select_band(self, x, mu, sigma):

        if x <= (mu-sigma):
            return "Band 1"
        elif x >= (mu+sigma):
            return "Band 3"
        return "Band 2"

    def allocate_bands(self):

        self.compute_gds_stdev()

        mu = statistics.mean(self.scored_df['gds_score'])
        sigma = statistics.stdev(self.scored_df['gds_score'])

        self.scored_df['band'] = self.scored_df['gds_score'].apply(lambda x: self.select_band(x, mu, sigma))

        return self.scored_df

def compute_score(program, course_list):

    # get dictionary
    label_dictionary = pd.read_csv("data/labelled_units_words.csv")

    # make dataframe
    course_list = course_list.split(',')
    course_list = [course.lower().strip() for course in course_list]
    df = pd.DataFrame(
        {
            'compulsory course': course_list, 
        }
    )
    df['url'] = program


    # score programs
    ps = ProgramScorer(label_dictionary, df)
    gds_scored_program = ps.score_programs_by_gds()
    sn = ScoreNormalizer(gds_scored_program)
    gds_scored_program_normalized = sn.update_scored_df()

    gds_scored_program_normalized = gds_scored_program_normalized.drop([
        'url',
        'Not determinable'
    ], axis=1)

    return gds_scored_program_normalized

def rank_programs(df, priority):

    # make priority dictionary
    priority_dic = {
        '1': 0,
        '2': 0,
        '3': 0,
        '4': 0,
        '5': 0,
        '6': 0
    }
    priority_list = priority.split(',')
    priority_list = [priority.strip() for priority in priority_list]
    start_score = 64
    for priority in priority_list:
        priority_dic[priority] = start_score
        start_score /= 2

    # get division weights
    weights = list(priority_dic.values())
    weights = [int(weight) for weight in weights]
    weights = np.c_[weights]
    
    # get the GDS proportion matrix
    gds_prop_matrix = df[[
        "Data Gathering, Preparation and Exploration",
        "Data Representation and Transformation",
        "Computing with Data",
        "Data Modeling",
        "Data Visualization and Presentation",
        "Science about Data Science",
    ]].to_numpy()

    # get the weighted GDS score
    weighted_gds_score = np.matmul(gds_prop_matrix, weights)
    df['weighted'] = weighted_gds_score
    df = df.sort_values(by="weighted", ascending=False).reset_index(drop=True)

    return df

class ProgramRecommender:

    def __init__(self, df):

        pgm_id = df['uni_name'] + " - " + df['pgm_name']
        descr = df['descr']
        text = df['descr'].apply(lambda x: TextPreprocessor(x).preprocess_text() if x!='Not inferred' else x)
        self.df_gds = df[[
            "id",
            "Data Gathering, Preparation and Exploration",
            "Data Representation and Transformation",
            "Computing with Data",
            "Data Modeling",
            "Data Visualization and Presentation",
            "Science about Data Science",
        ]]

        self.df_descr = pd.DataFrame({
            'id': pgm_id,
            'descr': descr,
            'text': text
        })

        # vectorize program descriptions
        tfidf = TfidfVectorizer(
            stop_words=STOP_WORDS
        )
        tfidf_df_descr = tfidf.fit_transform(self.df_descr['text'])

        # make the main dataset
        prog_descr_df = pd.DataFrame(tfidf_df_descr.todense(), columns=tfidf.get_feature_names())
        self.dataset = pd.concat([self.df_gds, prog_descr_df], axis=1)

        # compute similarity matrix
        features = self.dataset.drop(['id'], axis=1)
        self.cosine_sim_programs = cosine_similarity(features)

    def get_id_from_index(self, idx):
        return self.dataset[self.dataset.index == idx]['id'].values[0]

    def get_index_from_id(self, pgm_id):
        return self.dataset[self.dataset['id'] == pgm_id].index.values[0]

    def get_most_similar(self, pgm_name, npgms=5):
        pgm_index = self.get_index_from_id(pgm_name)
        similar_pgms = list(enumerate(self.cosine_sim_programs[pgm_index]))
        sorted_similar_pgms = sorted(similar_pgms,key=lambda x:x[1],reverse=True)[1:]

        top_n_pgms = sorted_similar_pgms[:npgms]
        
        return ([self.get_id_from_index(idx[0]) for idx in top_n_pgms]) 

    










