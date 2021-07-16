import os
import pandas as pd
from gds_operations import ProgramScorer, ScoreNormalizer


if __name__ == '__main__':

    label_dictionary = pd.read_csv('labelled_words.csv')

    data_path = "../../data_collection/data/processed"
    pgm_india = pd.read_csv(os.path.join(data_path, "india_pgms.csv")).fillna("Not inferred")
    pgm_usa = pd.read_csv(os.path.join(data_path, "usa_pgms.csv")).fillna("Not inferred")
    curr_india = pd.read_csv(os.path.join(data_path, "india_curr.csv")).fillna("Not inferred")
    curr_usa = pd.read_csv(os.path.join(data_path, "usa_curr.csv")).fillna("Not inferred")
    curr_usa = curr_usa.drop(['Unnamed: 4', 'Unnamed: 5'], axis=1)

    curr_india = curr_india.drop(['course outcome or overview', 'topics covered'], axis=1)
    curr_usa = curr_usa.drop(['course outcome or overview', 'topics covered'], axis=1)

    # score programs by gds
    ps = ProgramScorer(label_dictionary, curr_india)
    gds_scored_programs = ps.score_programs_by_gds()
    sn = ScoreNormalizer(gds_scored_programs)
    gds_scored_programs_normalized_india = sn.update_scored_df()

    ps = ProgramScorer(label_dictionary, curr_usa)
    gds_scored_programs = ps.score_programs_by_gds()
    sn = ScoreNormalizer(gds_scored_programs)
    gds_scored_programs_normalized_usa = sn.update_scored_df()

    # merge with programs
    df_india = pd.merge(
        pgm_india,
        gds_scored_programs_normalized_india,
        on='url'
    )
    df_india['country'] = "India"

    df_usa = pd.merge(
        pgm_usa,
        gds_scored_programs_normalized_usa,
        on='url'
    )
    df_usa['country'] = "USA"

    # combine both dataframes
    df = pd.concat([df_india, df_usa])

    # save the file
    df.to_csv('../../data_collection/data/labelled/academic_data.csv', index=False)


    