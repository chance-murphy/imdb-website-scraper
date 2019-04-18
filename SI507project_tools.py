# __author__ = "Chance Murphy"

from datetime import datetime
from bs4 import BeautifulSoup # need beautifulsoup for scraping
import requests, json # need these to access data on the internet and deal with structured data in my cache
import pandas as pd
import csv

# Caching Structure imported from advanced_expiry_caching.py file on Cavas.

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
DEBUG = True

class Cache:
    def __init__(self, filename):
        """Load cache from disk, if present"""
        self.filename = filename
        try:
            with open(self.filename, 'r') as cache_file:
                cache_json = cache_file.read()
                self.cache_diction = json.loads(cache_json)
        except:
            self.cache_diction = {}

    def _save_to_disk(self):
        """Save cache to disk"""
        with open(self.filename, 'w') as cache_file:
            cache_json = json.dumps(self.cache_diction)
            cache_file.write(cache_json)

    def _has_entry_expired(self, timestamp_str, expire_in_days):
        """Check if cache timestamp is over expire_in_days old"""

        # gives current datetime
        now = datetime.now()

        # datetime.strptime converts a formatted string into datetime object
        cache_timestamp = datetime.strptime(timestamp_str, DATETIME_FORMAT)

        # subtracting two datetime objects gives you a timedelta object
        delta = now - cache_timestamp
        delta_in_days = delta.days


        # now that we have days as integers, we can just use comparison
        # and decide if cache has expired or not
        if delta_in_days > expire_in_days:
            return True # It's been longer than expiry time
        else:
            return False

    def get(self, identifier):
        """If unique identifier exists in the cache and has not expired, return the data associated with it from the request, else return None"""
        identifier = identifier.upper() # Assuming none will differ with case sensitivity here
        if identifier in self.cache_diction:
            data_assoc_dict = self.cache_diction[identifier]
            if self._has_entry_expired(data_assoc_dict['timestamp'],data_assoc_dict['expire_in_days']):
                if DEBUG:
                    print("Cache has expired for {}".format(identifier))
                # also remove old copy from cache
                del self.cache_diction[identifier]
                self._save_to_disk()
                data = None
            else:
                data = data_assoc_dict['values']
        else:
            data = None
        return data

    def set(self, identifier, data, expire_in_days=7):
        """Add identifier and its associated values (literal data) to the cache, and save the cache as json"""
        identifier = identifier.upper() # make unique
        self.cache_diction[identifier] = {
            'values': data,
            'timestamp': datetime.now().strftime(DATETIME_FORMAT),
            'expire_in_days': expire_in_days
        }

        self._save_to_disk()

FILENAME = "movies_search_cache.json" # saved in variable with convention of all-caps constant

program_cache = Cache(FILENAME) # create a cache -- stored in a file of this name

url = "https://www.imdb.com/search/title?title_type=feature,&num_votes=1000,&languages=en&sort=user_rating,desc" #url can act as identifier for caching in a scraping situation -- it IS frequently unique here, unlike in query requests

data = program_cache.get(url)
if not data: # use the .get function from the Cache class to see if we can get this data from the cache -- do we already have data associated with this url? if not,
    # make a request to get the data from the internet -- all the junk at that page
    data = requests.get(url).text # get the text attribute from the Response that requests.get returns -- and save it in a variable. This should be a bunch of html and stuff
    #print(data) # to prove it - this will print out a lot

    # set data in cache:
    program_cache.set(url, data, expire_in_days=1) # just 1 day here because news site / for an example in class

# now data stored in variable -- can do stuff with it, separate from the caching
soup = BeautifulSoup(data, "html.parser") # html.parser string argument tells BeautifulSoup that it should work in the nice html way

#print(soup.prettify()) # view the "pretty" version of everything in the BeautifulSoup instance

#print(soup.find_all("a")) # see if this works...

# All the list items on the page
# print(list_items) # to see


movie_titles = [] # gotta get all the data in BeautifulSoup objects to work with...
release_dates = []
runtimes = []
ratings = []
directors = []
IMDB_ratings = []
box_office = []
metascores = []

titles =  soup.find_all('div',{'class':'lister-item-content'})
for i in titles:
    title = i.h3.a.text
    movie_titles.append(title)

released = soup.find_all('span',{'class':'lister-item-year'})
for i in released:
    release = i.text
    release_dates.append(release)

times = soup.find_all('span',{'class':'runtime'})
for i in times:
    time = i.text
    runtimes.append(time)

rating = soup.find_all('span',{'class':'certificate'})
for i in rating:
    rating = i.text
    ratings.append(rating)

### STILL TRYING TO SCRAPE DIRECTOR ###
# director = soup.find_all('div',{'class':'lister-item-content'})
# for i in director:
#     name = i.a.text
#     ratings.append(name)

imdb = soup.find_all('div',{'class':'ratings-bar'})
for i in imdb:
    i_rating = i.strong.text
    IMDB_ratings.append(i_rating)

meta = soup.find_all('span',{'class':'metascore'})
for i in meta:
    metascore = i.text
    metascores.append(metascore)

# print(movie_titles)
# print(release_dates)
# print(runtimes)
# print(ratings)
# print(directors)
# print(IMDB_ratings)
# print(metascores)

print(len(movie_titles))
print(len(release_dates))
print(len(runtimes))
print(len(ratings))
# print(len(directors))
print(len(IMDB_ratings))
print(len(metascores))

# movie_info = pd.DataFrame({'Title': movie_titles,
#                        'Rating': ratings,
#                        'IMDB Rating': IMDB_ratings,
#                        'Metascore': metascores,
#                        'Release Date': release_dates,
#                        'Runtime': runtimes,
# })
#
# csv_file_name = "movie_info.csv"
#
# site_info.to_csv(csv_file_name)
