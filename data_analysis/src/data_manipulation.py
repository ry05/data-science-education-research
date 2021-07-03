""" 
Data Manipulation Module

Functions to manipulate data
"""

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