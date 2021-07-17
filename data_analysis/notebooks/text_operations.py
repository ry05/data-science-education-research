import os
import string
import re

import pandas as pd
import statistics
import spacy
import textstat
from lexicalrichness import LexicalRichness
from spacy.lang.en.stop_words import STOP_WORDS
nlp = spacy.load("en_core_web_md")


class TextPreprocessor:

    def __init__(self, text):
        self.text = text

    def make_lowercase(self):
        self.text = self.text.lower()

    def remove_numbers(self):
        self.text = self.text.translate({ord(k): ' ' for k in string.digits})

    def remove_unnecessary_whitespace(self):
        self.text = self.text.replace('\t', '').replace('\n', '')
        self.text = re.sub(' +', ' ', self.text)
        self.text = self.text.strip()

    def remove_urls(self):
        self.text = re.sub(r'http\S+', ' ', self.text)

    def remove_punctuations(self):
        self.text = self.text.translate({ord(k): ' ' for k in string.punctuation})

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

class ComplexityComputer:
    """
    Extracts textual complexity
    """

    def __init__(self, text):
        self.text = text
        self.doc = nlp(text)
        self.sentences = list(self.doc.sents)
        self.tokens = [token for token in self.doc] # send to final
        self.words = [token for token in self.tokens if not(token.is_punct or token.is_digit)]
        self.numeric = [token for token in self.tokens if token.like_num]
        self.chars_per_word = [len(token.text) for token in self.words]
        self.words_per_sent = [len([token for token in sent if not(token.is_digit or token.is_punct)]) for sent in self.sentences]

    def __str__(self):
        return self.text
    
    def count_units(self):
        self.char_cnt = len(self.text)
        self.word_cnt = len(self.words)
        self.sent_cnt = len(self.sentences)
        self.digits_cnt = len(self.numeric)

    def compute_ratios(self):
        self.mean_chars_per_word = statistics.mean(self.chars_per_word)
        self.median_chars_per_word = statistics.median(self.chars_per_word)
        self.mean_words_per_sent = statistics.mean(self.words_per_sent)
        self.median_words_per_sent = statistics.median(self.words_per_sent)

    def compute_pos(self):
        self.common_nouns = [token for token in self.doc if token.pos_ == "NOUN"]
        self.proper_nouns = [token for token in self.doc if token.pos_ == "PROPN"]
        self.adjectives = [token for token in self.doc if token.pos_ == "ADJ"]
        self.verbs = [token for token in self.doc if token.pos_ == "VERB"]
        self.numerals = [token for token in self.doc if token.pos_ == "NUM"]

    def prop_pos_units(self):
        self.common_nouns_prop = len(self.common_nouns) / self.word_cnt
        self.proper_nouns_prop = len(self.proper_nouns) / self.word_cnt
        self.adjectives_prop = len(self.adjectives) / self.word_cnt
        self.verbs_prop = len(self.verbs) / self.word_cnt
        self.numerals_prop = len(self.numerals) / self.word_cnt
           
    def compute_readability(self):
        self.flesch_kincaid = textstat.flesch_kincaid_grade(self.text)
        self.dale_chall = textstat.dale_chall_readability_score(self.text)       

    def lexical_diversity_mtld(self):
        lex = LexicalRichness(self.text)
        self.mtld = lex.mtld()

    def compute_complexity(self):
        self.count_units()
        self.compute_ratios()
        self.compute_pos()
        self.count_pos_units()
        self.compute_readability()
        self.lexical_diversity_mtld()

    def get_complexity_measures(self):
        self.compute_complexity()
        measure_dict = dict(
            text = [self.text],
            char_cnt = [self.char_cnt],
            word_cnt = [self.word_cnt],
            sent_cnt = [self.sent_cnt],
            digits_cnt = [self.digits_cnt],
            mean_chars_per_word = [self.mean_chars_per_word],
            median_chars_per_word = [self.median_chars_per_word],
            mean_words_per_sent = [self.mean_words_per_sent],
            median_words_per_sent = [self.median_words_per_sent],
            common_nouns_prop = [self.common_nouns_prop],
            proper_nouns_prop = [self.proper_nouns_prop],
            adjectives_prop = [self.adjectives_prop],
            verbs_prop = [self.verbs_prop],
            numerals_cnt_prop = [self.numerals_cnt_prop],
            flesch_kincaid = [self.flesch_kincaid],
            dale_chall = [self.dale_chall],
            mtld = [self.mtld]
        )

        return (pd.DataFrame(measure_dict))

class CourseNamesProcessor:

    def __init__(self, course_list):
        self.courses = course_list

    def remove_duplicates(self):
        self.courses =  list(set(self.courses))

    def remove_punctuations(self, course):
        return course.translate({ord(k): ' ' for k in string.punctuation})

    def remove_numbers(self, course):
        return course.translate({ord(k): ' ' for k in string.digits})

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
    