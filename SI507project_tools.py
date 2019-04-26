# __author__ = "Chance Murphy"

import requests, json
from datetime import datetime
from bs4 import BeautifulSoup
import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

import pandas as pd
import csv

import os
from flask import Flask, render_template, session, redirect,request, url_for # tools that will make it easier to build on things
from flask_sqlalchemy import SQLAlchemy # handles database stuff for us - need to pip install flask_sqlalchemy in your virtual env, environment, etc to use this and run this

# import plotly
#
# plotly.tools.set_credentials_file(username='chancem', api_key='VYcQGpcVn8MufuWnvsVf')

# Application configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string for app security and movies and stuff and adgsdfsadfdflsdfsj'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./movies_results.db' # TODO: decide what your new database name will be -- that has to go here
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up Flask debug stuff

# class Director(db.Model):
#     __tablename__ = "directors"
#     id = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(64))
#     Movies = db.relationship('Movie',secondary = collections,backref=db.backref('director1',lazy='dynamic'),lazy='dynamic')

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
descriptions = []
ratings = []
box_office = []
num_votes = []
IMDB_ratings = []
directors = []
metascores = []
genres = []

movies_list = soup.find_all('div',{'class':'lister-item-content'})

# print(len(movies_list))

for i in movies_list:

    # Get the title of each movie
    title = i.h3.a.text
    movie_titles.append(title)

    # Get the release date of each movie
    release = i.find('span',{'class':'lister-item-year'})
    release_dates.append(release.text)

    # Get the runtime data for each movie,  if no data exists clean and replace with 'N/A'
    time = i.find('span',{'class':'runtime'})
    # time = runtime.text
    if time == None:
        time = 'N/A'
        runtimes.append(time)
    else:
        runtimes.append(time.text)

    # Get the MPAA Rating of each movie, if no data exists clean and replace with "N/A'"
    rating = i.find('span',{'class':'certificate'})
    # time = runtime.text
    if rating == None:
        rating = 'N/A'
        ratings.append(rating)
    else:
        ratings.append(rating.text)

    # Get the total number of votes for each movies IMDB rating
    votes_gross = i.find_all('span',{'name':'nv'})
    votes = votes_gross[0]
    num_votes.append(votes.text)

    # Get the Gross Box Office total for each movie, if none exists clean and replace with 'N/A'
    if len(votes_gross) == 2:
        gross = votes_gross[1]
        box_office.append(gross.text)
    else:
        gross = 'N/A'
        box_office.append(gross)

    # Get the IMDB Rating of each movie
    imdb = i.find('div',{'class':'ratings-imdb-rating'})
    IMDB_ratings.append(imdb.strong.text)

    # Get the Metascore of each movie, if none exists clean and replace with 'N/A'
    meta = i.find('span',{'class':'metascore'})
    if meta == None:
        meta = 'N/A'
        metascores.append(meta)
    else:
        metascores.append(meta.text)

    # Get the director of each movie
    p_elements = i.find_all('p')
    p = p_elements[2]
    a_elements = p.find_all('a')
    director = a_elements[0]
    directors.append(director.text)

    # Get the description of each movie
    p_text = i.find_all('p',{'class':'text-muted'})
    about = p_text[1]
    descriptions.append(about.text)

    # Get the genre of each movie
    genre = i.find('span',{'class':'genre'})
    genres.append(genre.text)


# print(movie_titles)
# print(release_dates)
# print(runtimes)
# print(ratings)
# print(box_office)
# print(num_votes)
# print(directors)
# print(IMDB_ratings)
# print(metascores)
# print(descriptions)
# print(genres)

## Checking make sure the length of each list is 50 so Pandas can use all the data.
#
# print(len(movie_titles))
# print(len(release_dates))
# print(len(runtimes))
# print(len(ratings))
# print(len(box_office))
# print(len(num_votes))
# print(len(directors))
# print(len(IMDB_ratings))
# print(len(metascores))
# print(len(descriptions))
# print(len(genres))

##
## Create DB
##

db = SQLAlchemy(app) # For database use
session = db.session # to make queries easy

class Movies(db.Model):
    __tablename__ = "Movies"
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(64))
    ReleaseDate = db.Column(db.String(64))
    Director = db.Column(db.String(64))
    Genre = db.Column(db.String(64))
    Description = db.Column(db.String(1000))
    MPAARating = db.Column(db.String(64))
    RunTime = db.Column(db.String(64))

    def __repr__(self):
        return "{}: {} is a {} movie released in {} and directed by {}. It recieved an MPAA rating of {} and has a runtime of {}. \n Short Description: {}\n".format(self.id,self.Title,self.Genre,self.ReleaseDate,self.Director,self.MPAARating,self.RunTime,self.Description)

class Ratings(db.Model):
    __tablename__ = "Ratings"
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(64), db.ForeignKey("Ratings.Title"))
    IMDBRating = db.Column(db.String(64))
    Votes = db.Column(db.String(64))
    Metascore = db.Column(db.String(64))

    def __repr__(self):
        return "{}: {} has an IMDB rating of {} based on {} user ratings. It's Metascore is {}\n".format(self.id,self.Title,self.IMDBRating,self.Votes,self.Metascore)

##
## Import data to CSV via pandas
##

movie_info = pd.DataFrame({'Title': movie_titles,
                       'Director': directors,
                       'Release Date': release_dates,
                       'Run Time': runtimes,
                       'Genre': genres,
                       'MPAA Rating': ratings,
                       'Description': descriptions,
                       'IMDB Rating': IMDB_ratings,
                       'Number of Votes': num_votes,
                       'Metascore': metascores,
})

csv_file_name = "movie_info.csv"

movie_info.to_csv(csv_file_name)


def add_to_db():
    with open("movie_info.csv", "r") as f:
        reader = csv.reader(f)
        data = []
        for i in reader:
            data.append(i)
    #print(len(data))

    for i in data[1:]:
        movie = Movies(Title = i[1],ReleaseDate = i[3],Director = i[2],Genre = i[5],Description = i[7],MPAARating = i[6],RunTime = i[4])
        rating = Ratings(Title = i[1],IMDBRating = i[8],Votes = i[9],Metascore = i[10])

        session.add(movie)
        session.add(rating)
        session.commit()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/search_results')
def results():
    if request.method == 'GET':
        keyword = request.args.get('keyword')
        # no = request.args.get('no')
        keyword = keyword if keyword else 'End Game'
        # no = no if no else 10  # use 10 as default value
        results = session.query(Movies).all()
        results_lst = []
        for i in results:
            if keyword in i.Title:
                results_lst.append(i)
            if keyword in i.Director:
                results_lst.append(i)
        return render_template('results.html',keyword = keyword, results = results_lst)

@app.route('/movies')
def movies():
    movies = Movies.query.all()
    movies_str= list(map(lambda x: str(x), movies))
    return render_template('movies.html', results = movies_str)

@app.route('/ratings')
def ratings():
    ratings = Ratings.query.all()
    ratings_str= list(map(lambda x: str(x), ratings))
    return render_template('ratings.html', results = ratings_str)

# # Create scatter plot of IMDB ratings using Plotly
#
# trace = go.Scatter(x = num_votes, y = IMDB_ratings, mode = 'markers')
#
# data = [trace]
#
# py.iplot(data, filename='IMDB_ratings_scatter')

if __name__ == '__main__':
    db.drop_all()
    db.create_all() # This will create database in current directory, as set up, if it doesn't exist, but won't overwrite if you restart - so no worries about that
    add_to_db()
    app.run() # run with this: python main_app.py runserver
