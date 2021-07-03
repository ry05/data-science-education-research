""" 
Module Scraper

Implementation of the Universal Web Scraper
"""


import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import re
from collections import defaultdict, Counter
from htmldate import find_date

import warnings
warnings.filterwarnings('ignore')

"""

def get_curriculum_table(url, useful_area_path=None, component=0, remove_row_idx=[]):

    try:
        response = requests.get(
            url,
            #params = {'PG':page_num},
            headers = {'User-agent': 'DSE Scraper'},
            timeout=(5,5)
        )
    except:
        print(f'Connection dropped')

    soup = BeautifulSoup(response.content, 'html.parser')
    soup_refined = soup.select(useful_area_path)[component]

    # get data from the table
    #remove_row_idx = [1,2,11,12,13] # added in by inspection by the user
    rows = soup_refined.find_all("tr")
    data_row = []
    idx = 1
    for r in rows:
        if idx not in remove_row_idx:
            data_row.append(r.text)
        idx += 1

    # clean up data
    num_ptrn = r'[0-9]'
    data_row = [re.sub(num_ptrn, '', d).replace('\n', '; ').replace('/', '').strip('; ').split('; ') for d in data_row]
    data_row = [course for data in data_row for course in data]
    data_row = [course for course in data_row if len(course)!=0]
    data_row[:10]

    # make dataframe
    courses_taught = pd.DataFrame(
        dict(
            compulsory_course = data_row
        )
    )
    return courses_taught

def get_tag_frequencies(url):

    try:
        response = requests.get(
            url,
            headers = {'User-agent': 'DSE Scraper'},
            timeout=(5,5)
        )
    except:
        print(f'Connection dropped')

    soup = BeautifulSoup(response.content, 'html.parser')

    # get count of all tag occurences
    all_tags = [tag.name for tag in soup.find_all(True)]
    tag_freq_occ = dict(Counter(all_tags))

    return tag_freq_occ

def get_emphasized_elements(url):

    emphasized = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'b', 'strong', 'i', 'em', 'mark']
    # from http://www.simplehtmlguide.com/text.php

    try:
        response = requests.get(
            url,
            headers = {'User-agent': 'DSE Scraper'},
            timeout=(5,5)
        )
    except:
        return 'Not inferred'

    soup = BeautifulSoup(response.content, 'html.parser')

    # get emphasized elements
    emp_data = soup.find_all(emphasized)
    emp_data = [ele.text.replace('\xa0', '').replace('\n', '').strip().lower() for ele in emp_data]
    emp_data = [ele for ele in emp_data if (ele != '' and ele != '\xa0')]
    uniq_emp_data = list(set(emp_data))
    
    return uniq_emp_data

"""


class Program:

    def __init__(self, url=None, driver_path=None, useful_area_path=None, static=True):

        self.url = url
        self.driver_path = driver_path
        self.useful_area = useful_area_path
        self.static = static
        self.header_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        self.content_tags = ['p', 'ul', 'ol']
        self.link_tags = ['a']
        self.emphasized = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'b', 'strong', 'i', 'em', 'mark']
        # from http://www.simplehtmlguide.com/text.php

        self.response = None
        self.headers_dict = defaultdict(list)
        self.links = []
        self.tags_present = []
        self.tags_frequencies = None
        self.emphasized_elements = None
        self.text = None
        self.published = None
        self.last_modified = None

    def get_response(self):

        response = requests.get(
            self.url,
            headers = {'User-agent': 'DSE Scraper'},
            timeout=(10,10),
            verify=False
        )

        if response.status_code == 200:
            self.response = response
        else:
            print (response.status_code)
            print('Not a successful response')

    def start_driver(self):

        self.driver = webdriver.Chrome(self.driver_path)
        self.driver.get(self.url)
        time.sleep(5)
        print("Opened home webpage")

    def get_useful_area(self, parse=None):

        if parse != None:

            self.soup_refined = parse

        else:

            if self.static:
                self.get_response()
                soup = BeautifulSoup(self.response.content, 'html.parser')

            else:
                self.start_driver()
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            # refine to get useful area
            self.soup_refined = soup.select(self.useful_area)[0]

    def get_header_content(self):

        headers = self.soup_refined.find_all(self.header_tags)
        for h in headers:
            self.headers_dict[h.name].append(h.text)

    def get_content(self):

        flattened_headers = [h for sub in list(self.headers_dict.values()) for h in sub]
        contents = self.soup_refined.find_all(self.content_tags+self.header_tags)
        self.text = ' '.join(['<'+c.text+'>' if c.text in flattened_headers else c.text for c in contents]) + '<'

    def get_links(self):

        for link in self.soup_refined.find_all(self.link_tags, href=True):
            if link['href'] not in self.links:
                self.links.append(link['href'])
                #self.links = '; '.join(list(self.links))

        if len(self.links) == 0:
            self.links = 'no links in useful area'

    def get_tag_frequencies(self):

        # get count of all tag occurences
        self.tags_present = [tag.name for tag in self.soup_refined.find_all(True)]
        self.tags_frequencies = dict(Counter(self.tags_present))

    def get_emphasized_elements(self):

        # get emphasized elements
        emp_data = self.soup_refined.find_all(self.emphasized)
        emp_data = [ele.text.replace('\xa0', '').replace('\n', '').strip().lower() for ele in emp_data]
        emp_data = [ele for ele in emp_data if (ele != '' and ele != '\xa0')]
        self.emphasized_elements = list(set(emp_data))
    
    def get_date(self):

        try:
            self.published = find_date(self.url, original_date=True)
        except:
            self.published = 'Not inferred'

        try:
            self.last_modified = find_date(self.url)
        except:
            self.last_modified = 'Not inferred'

        #return (self.published, self.last_modified)

    def extract_df(self, content=True, pass_parse=None):

        self.get_useful_area(parse=pass_parse)
        self.get_header_content()
        self.get_content()
        self.get_links()
        self.get_tag_frequencies()
        self.get_emphasized_elements()
        self.get_date()

        heads = (re.findall("<([^>]*)>", self.text))
        text = (re.findall(">([^<]*)<", self.text))

        if content:

            self.content_df = pd.DataFrame(
                dict (
                    url = self.url,
                    header = heads,
                    content = text,
                )
            )

            return self.content_df

        else:

            temp_dict = dict (
                    url = self.url,
                    header_tag = list(self.headers_dict.keys()),
                    header_names = list(self.headers_dict.values()),
                    links_useful_area = self.links,
                    tags = self.tags_present,
                    tag_freq = self.tags_frequencies,
                    emphasized = self.emphasized_elements,
                    date_published = self.published,
                    date_last_modified = self.last_modified
                )

            self.structure_df = pd.DataFrame.from_dict(temp_dict, orient='index').transpose()

            return self.structure_df

        if not self.static:
            self.driver.quit()



    