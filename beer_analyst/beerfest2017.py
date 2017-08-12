# -*- coding: utf-8 -*-
"""
Using ratebeer_scraper, get a list of beer/cider ratings from the Halifax
Beerfest 2017.
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from ratebeer_scraper import get_beer_data,search_ratebeer

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



get_urls = False
if get_urls:
    google_search_url = ["https://www.google.ca/search?q=",
                         "+site%3Aratebeer.com"]
    #beerfest_ratings_df = beerfest_df.copy()
    #beerfest_ratings_df["search_query"] = ""
    #beerfest_ratings_df["br_url"] = None
    for i,beer_df in beerfest_ratings_df.iterrows():
        if beer_df.br_url is None:
            search_query = ' '.join([beer_df.brewery, beer_df.beer_name])
            beerfest_ratings_df.set_value(i, "search_query", search_query)
            page = requests.get(google_search_url[0] + search_query + \
                                google_search_url[1])
            if page.status_code == 503:
                print(i, beer_df.beer_name)
                print("Status code 503")
                break
            try:
                print(search_query)
                soup = BeautifulSoup(page.text, "lxml")
                br_url = soup.find('h3', class_ = 'r').a['href'][7:]
                if br_url[0:30] != "https://www.ratebeer.com/beer/":
                    br_url = "NA"
                
                beerfest_ratings_df.set_value(i, "br_url", br_url)
            except:
                search_query = beer_df.beer_name
                beerfest_ratings_df.set_value(i, "search_query", search_query)
                page = requests.get(google_search_url[0] + search_query + \
                                    google_search_url[1])
                if page.status_code == 503:
                    print(i, beer_df.beer_name)
                    print("Status code 503")
                    break
                try:
                    print(search_query)
                    soup = BeautifulSoup(page.text, "lxml")
                    br_url = soup.find('h3', class_ = 'r').a['href'][7:]
                    if br_url[0:30] != "https://www.ratebeer.com/beer/":
                        br_url = "NA"
                    beerfest_ratings_df.set_value(i, "br_url", br_url)
                except:
                    print("Failed: ", search_query)
        else:
            print("Skipping: ", i, beer_df.beer_name)
    
    # Manually edit/fix certain urls
    beerfest_ratings_df.set_value(312, "br_url", 
        "https://www.ratebeer.com/beer/erdinger-oktoberfest-weizen/48060/")


get_ratings = True
if get_ratings:
    for i,beer_df in beerfest_ratings_df.iterrows():
        print(i, beer_df.beer_name)
        
        br_url = beer_df.br_url
        if br_url is None or br_url == "NA":
            br_df = pd.DataFrame([[None] * len(br_df.columns)],
                                  columns = br_df.columns)
        else:
            br_df = get_beer_data(br_url)
        if i == 0:
            results_df = br_df
        else:
            results_df = results_df.append(br_df, ignore_index = True)
    beerfest_ratings_df2 = pd.concat([beerfest_ratings_df, results_df],
                                    axis = 1)
    
        
all_beers = beerfest_ratings_df2[["category", "brewery", "beer_name",
                                  "abv", "rb_name", 
                                  "rb_overall_rating", "rb_weighted_avg",
                                  "rb_ratings",
                                  "rb_style", "rb_style_rating"]]. \
                                  sort_values(["rb_overall_rating", "rb_ratings"],
                                       ascending = [0, 0])
all_beers.to_csv("tables/beerfest2017.csv")

all_ciders = all_beers.loc[all_beers.category == "Cider"]
all_ciders.to_csv("tables/beerfest2017_ciders.csv")

all_beers_brewery_order = all_beers.sort_values(["brewery", "beer_name"])
all_beers_brewery_order.to_csv("tables/beerfest2017_breweries.csv")