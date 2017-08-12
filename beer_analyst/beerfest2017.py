# -*- coding: utf-8 -*-
"""
Using ratebeer_scraper, get a list of beer/cider ratings from the Halifax
Beerfest 2017.
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from ratebeer_scraper import search_ratebeer

url = "https://seaportbeerfest.com/breweries"
page = requests.get(url)
soup = BeautifulSoup(page.text, "lxml")

beerfest_df = pd.DataFrame(columns = ["category", "brewery", "beer_name", "abv"])

category_list = soup.findAll("div", {"class" : "accordion"})
for category_div in category_list:
    category = ' '.join(category_div.h3.get_text().split(' ')[0:-1])
    #print(category)
    brewery_list = category_div.findAll("div", {"class": "views-row"})
    for brewery_div in brewery_list:
        brewery_header = brewery_div.find("span", {"class": "field-content"})
        if brewery_header:
            brewery = brewery_header.get_text().split(' (')[0].strip()
            #print(brewery)
            beer_list = brewery_div.findAll("div",
                                {"class": "views-field-field-beer-name"})
            for beer_div in beer_list:
                beer_abv = beer_div.get_text().strip().split(' ')
                if len(beer_abv) > 1:
                    abv = beer_abv[-1]
                    beer_name = ' '.join(beer_abv[0:-1])
                    #print(category, brewery, beer_name, abv)
                    beerfest_df = beerfest_df.append({"category": category,
                                                      "brewery": brewery,
                                                      "beer_name": beer_name,
                                                      "abv": abv},
                                                       ignore_index = True)

# The following search queries return >1 result
# The keys of this dict are search queries (brewery + beer name), while the
#  values are either integers (which of the returned list is the correct beer)
#  or a string to be used as an alternate search query
multiple_results = {
    "Glutenberg Glutenberg IPA": "Glutenberg IPA ASAP",
    "Tempted Cider Sweet Cider": 0,
    "Tempted Cider Dry Cider": "Tempted? Irish Craft Cider Medium Dry",
    "Trois Mousquetaires Oud Bruin": "Les Trois Mousquetaires Hors Série Oud Bruin",
    "Trois Mousquetaires Sticke Alt": "Les Trois Mousquetaires S.S. Sticke Alt",
    "Trou du Diable Willow Gose": 0,
    "Central City Red Racer IPA": 6,
    "Carlsberg Carlsberg Lager": 0,
    "Erdinger Weissbier": 1,
    "Mort Subite Kriek": 1,}
# These beers do not show up in the rate_beers database
skip = ["Bulwark Cider Raspberry",
        "Chainyard Cider Hopped Up"]

search_results = pd.DataFrame(columns = ["brewery", "beer_name",
                                         "query", "results"])
test = beerfest_df.iloc[0:5]
#for i,beer_df in beerfest_df.iterrows():
google_search_url = ["https://www.google.ca/search?q=",
                     "+site%3Aratebeer.com"]
for i,beer_df in test.iterrows():
    search_query = ' '.join([beer_df.brewery, beer_df.beer_name])
    page = requests.get(google_search_url[0] + search_query + \
                        google_search_url[1])
    soup = BeautifulSoup(page.text, "lxml")
    print(search_query, soup.find('cite').text)
    
    
    
    
if False:    
    search_query = ' '.join([beer_df.brewery, beer_df.beer_name])
    if search_query in skip:
        continue
    
    ratings_index = 0
    if search_query in multiple_results.keys():
        if str(multiple_results[search_query]).isdigit():
            ratings_index = multiple_results[search_query]
        else:
            search_query = multiple_results[search_query]
    print(search_query)
    ratings_df = search_ratebeer(search_query)
    # If no results, try a broader search with just the beer name
    if len(ratings_df) == 0:
        search_query = ' '.join([beer_df.brewery.split(' ')[0],
                                 beer_df.beer_name])
        ratings_df = search_ratebeer(search_query)
        if len(ratings_df) == 0:
            search_query = beer_df.beer_name
            ratings_df = search_ratebeer(search_query)
    
    if search_query in multiple_results.keys(): n_results = 1
    else: n_results = len(ratings_df)
    
    if n_results > 0:
        rating_df = ratings_df.iloc[ratings_index]
        result_name = rating_df.beer_name
    else: 
        result_name = "NA"
    search_results = search_results.append({"brewery": beer_df.brewery,
                                            "beer_name": beer_df.beer_name,
                                            "query": search_query,
                                            "results": n_results,
                                            "result_name": result_name},
                                            ignore_index = True)
                    
           
        
