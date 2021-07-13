import os

from collections import Counter
import pandas as pd
import numpy as np


class GDSClassifier:

    def __init__(self, labelled_dictionary_path, compulsory_course_data_path):

        self.dictionary = pd.read_csv(labelled_dictionary_path)
        self.data = pd.read_csv(compulsory_course_data_path)


    def __str__(self):

        print("Overview of GDS classifier object")
        print(f"Number of labelled words in dictionary: {len(self.dictionary)}")
        print(f"Number of non-missing compulsory courses in data file: {self.data[self.data.notnull()].shape[0]}")
    
def get_gds_labels_for_course(course_name, labelled_words = None):
    """Get the GDS labels for a course

    Args:
        course_name ([type]): [description]

    Returns:
        [type]: [description]
    """

    labels = ""

    if course_name == 'Not inferred':
        return x
    x = course_name.lower()
    for word, label in zip(list(labelled_words['word']), list(labelled_words['labels'])):
        if word in x:
            labels = labels + ";" + label

    return labels

def convert_gds_labels_string_to_list(gds_labels_as_string):
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

def confirm_gds_labels_existence(gds_labels_as_string):
    """Confirm whether a particular GDS label exists or not

    Args:
        gds_labels_as_string ([type]): [description]

    Returns:
        [type]: [description]
    """

    x = convert_gds_labels_string_to_list(gds_labels_as_string)
    
    gds_labels_confirmed_dict = Counter(x)

    return gds_labels_confirmed_dict

def split_gds_labels_into_features(gds_labels_confirmed_dict, label):
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