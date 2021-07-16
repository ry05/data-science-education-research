from collections import Counter
import pandas as pd 

from preprocess import TextPreprocessor

LABELS = [
    "Data Gathering, Preparation and Exploration",
    "Data Representation and Transformation",
    "Computing with Data",
    "Data Modeling",
    "Data Visualization and Presentation",
    "Science about Data Science",
    "Soft Skills",
    "Domain Specific",
    "Not determinable",
]

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
            list(self.dictionary['word']), list(self.dictionary['labels'])):
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

    def score_courses_by_gds(self):

        self.data["course_name_processed"] = self.data['compulsory course'].\
            apply(lambda x: TextPreprocessor(x).preprocess_text())
        self.data['gds_labels'] = self.data['course_name_processed'].apply(lambda x: self.get_gds_labels_for_course(x))
        self.data['gds_label_dict'] = self.data['gds_labels'].apply(self.confirm_gds_labels_existence)

        for label in self.labels:
            self.data[label] = None

        for label in self.labels:
            self.data[label] = self.data.gds_label_dict.apply(lambda x: self.get_status_label_existence(x, label))

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
                    'Soft Skills': 'sum',
                    'Domain Specific': 'sum',
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


