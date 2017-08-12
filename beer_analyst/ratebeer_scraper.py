import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
base_url = "http://www.ratebeer.com"

def search_ratebeer(search_query):
    """
    Returns a pandas dataframe of beers that match search_query.
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

    return beer_df

def get_beer_data(url):
    """
    Given a url to a ratebeer.com beer, returns information about it.
    """
    try:
        rb_page = requests.get(url)
        rb_soup = BeautifulSoup(rb_page.text, "lxml")
        
        rb_name = rb_soup.find(itemprop = "name").text.strip()
        rb_brewery = rb_soup.find_all('a', href=re.compile('brewers'))[1].text
        try:
            rb_overall_rating = int(rb_soup.find(class_='ratingValue').text)
        except:
            rb_overall_rating = None
        try:
            rb_style_rating = int(rb_soup.find(class_="style-text"). \
                                  previous_sibling.previous_sibling)
        except:
            rb_style_rating = None
        
        rb_style = rb_soup.find(text='Style: ').next_sibling.text
        
        rb_ratings = int(rb_soup.find('span', itemprop="ratingCount").text)
        
        try:
            rb_mean_rating = float(rb_soup.find(text='MEAN: '). \
                                   next_sibling.text.split('/')[0])
        except:
            rb_mean_rating = None
    
        try:
            rb_weighted_avg = float(rb_soup.find(text='WEIGHTED AVG: '). \
                                    next_sibling.text.split('/')[0])
        except:
            rb_weighted_avg = None
        
        beer_df = pd.DataFrame({"rb_url": url, "rb_name": rb_name,
                                "rb_brewery": rb_brewery,
                                "rb_overall_rating": rb_overall_rating,
                                "rb_style_rating": rb_style_rating,
                                "rb_style": rb_style,
                                "rb_ratings": rb_ratings,
                                "rb_mean_rating": rb_mean_rating,
                                "rb_weighted_avg": rb_weighted_avg},
                                index = [0])
        return beer_df
    except Exception as e:
        print(e)
        return None
    
 

