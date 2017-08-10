# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
#import json
from bs4 import BeautifulSoup

base_url = "http://www.ratebeer.com"

def search_ratebeer(search_query):
    """
    Returns a list of beers and breweries that match search_query
    """
    page = requests.get(base_url + "/findbeer.asp",
                        params = {"BeerName": search_query})
    soup = BeautifulSoup(page.text, "lxml")
    output = {"breweries": [], "beer": []}
    
    #table = soup.find('h2', string = 'beers')
    return soup