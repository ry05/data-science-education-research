""" 
Data Manipulation Module

Functions to manipulate data
"""

def get_degree(x):
    
    x = x.replace('(STEM)', '')
    if ' in ' in x.lower() and 'specialization' not in x.lower():
        temp = x.split(' in ')
    else:
        temp = x.split()

    subject = " ".join(temp[1:])
    return subject

def get_degree_2(x, sym):

    if sym in x.lower():
        temp = x.split(sym)
        subject = " ".join(temp[1:])
        
    else:
        subject = x

    subject = subject.replace(')', '').strip()
    
    return subject

def process_subject(i):
    alloted = False
    sub = []
    if 'data science' in i.lower():
        alloted = True
        sub.append('Data Science')
    if 'business analytics' in i.lower():
        alloted = True
        sub.append('Business Analytics')
    if ('analytics' in i.lower() or 'analysis' in i.lower()) and 'business analytics' not in i.lower():
        alloted = True
        sub.append('Analytics')
    if 'machine learning' in i.lower() or ' ml ' in i.lower():
        alloted = True
        sub.append('Machine Learning')
    if 'artificial intelligence' in i.lower() or ' ai ' in i.lower():
        alloted = True
        sub.append('Artificial Intelligence')
    if 'statistics' in i.lower():
        alloted = True
        sub.append('Statistics')
    if alloted == False:
        sub.append('Misc')
    return ", ".join(sub)

def process_dept(x):
    sub = []
    alloted = False
    if 'management' in x.lower() or 'business' in x.lower() or 'commerce' in x.lower():
        alloted = True
        sub.append('Management-related')
    if 'computer' in x.lower() or 'engineering' in x.lower() or 'info' in x.lower():
        alloted = True
        sub.append('Engineering-related')
    if 'data' in x.lower() or 'artificial intelligence' in x.lower() or 'machine learning' in x.lower():
        alloted = True
        sub.append('Data-related')
    if 'statistics' in x.lower() or 'math' in x.lower():
        alloted = True
        sub.append('Statistics-related')
    if 'social' in x.lower() or 'socio' in x.lower() or 'public' in x.lower() or 'politics' in x.lower():
        alloted=True
        sub.append('Social-related')
    if alloted == False:
        return 'Other'
    return ", ".join(sub)

def header_operations(htags, hnames):
    """Creates a dictionary matching header tags
    with header names

    Args:
        htags (pandas series): header tags
        hnames (pandas series): header tags' texts

    Returns:
        dict: mapping of header tag to associated texts
    """

    tag_name_dict = {}

    for tag, names in zip(htags, hnames):
        if tag == 'Not inferred':
            continue
        else:
            tag_name_dict[tag] = names

    return tag_name_dict