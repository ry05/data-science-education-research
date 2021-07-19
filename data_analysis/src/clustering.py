import pandas as pd


class FeatureSelection:
    """

    """

    def __init__(self, df):
        """
        df -> [id, text]
        """
        self.df = df

    def create_doc_term_matrix(self):

        pass

    def doc_freq_based(self):
        """
        - Remove stopwords
        - Remove words occuring in less than 1% of documents
        - Remove very frequent words (Tf-idf can help)
        """ 

        pass

    def lsi_based(self):

        pass
