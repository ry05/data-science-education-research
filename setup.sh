# COMMANDS TO SETUP THE PROJECT IN THE LOCAL SYSTEM

# install packages
pip install -r requirements.txt

python -m textblob.download_corpora

# download spacy trained model
python -m spacy download en_core_web_md

# run command to score the programs with GDS dictionary
python data_analysis/data_labeling/score_programs_by_gds.py