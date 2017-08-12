import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "http://www.ratebeer.com"

def search_ratebeer(search_query):
    """
    Returns a pandas dataframe of beers that match search_query
    """
    page = requests.get(base_url + "/findbeer.asp",
                        params = {"BeerName": search_query})
    soup = BeautifulSoup(page.text, "lxml")
    beer_df = pd.DataFrame(columns = ["beer_name", "rating", "num_ratings"])
    
    table = soup.find('h2', string = 'beers')
    if table:
        for row in table.next_sibling('tr'):
            if row.find(title = "Rate This Beer"):
                beer_name = row('td')[0].a.string.strip()
                beer_rating = row('td')[3].string
                num_ratings = row('td')[4].string
                
                beer_df = beer_df.append({"beer_name": beer_name,
                                          "rating": beer_rating,
                                          "num_ratings": num_ratings},
                                         ignore_index = True)
                #if beer_rating:
                #beer.overall_rating = int(overall_rating.strip())
                #if num_ratings:
                #beer.num_ratings = int(num_ratings.strip())
    return beer_df

