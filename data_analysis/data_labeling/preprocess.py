import os
import string
import re

import pandas as pd
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
nlp = spacy.load("en_core_web_md")


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

    def preprocess_text(self):

        self.make_lowercase()
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
    