# Chance Murphy 507 Final Project

Chance Murphy

[Link to this repository](https://github.com/chance-murphy/si-507-final-project)

---

## Project Description

This program has scraped the IMDB website to find the 50 movies with the highest IMDB ratings of all time. The program will cache the html of the IMDB search results page so that too many requests of the IMDB websites are not made. Once the data is cached, the HTML code is parsed with BeautifulSoup in order to pull out the data relating to each movie we want from the website. As the data is sifted through, it is cleaned to prevent empty cells in the CSV. With out data now sorted, located and cleaned Pandas is used to send the data to a CSV file. From here a function called "add_to_db" is called to open the CSV file and read the data into our database.

Now that all of the data is in the database, flask routes are used to display the data to the user. The routes allow the user to search the database for movies or directors as well as view all of the movies. Users can either view information about the movie (such as runtime, box office, release date, genre, etc.) or information about the movies IMDB or Metascore rating.

## How to run

1. Download all files from this Github repository.
2. Locate the zip file in your downloads folder and move it to a location easy to remeber, such as your desktop.
3. Open Terminal
4. Navigate to the folder
5. Create a virtual enviornament
  - In order to do this type in the following commands into your command prompt/terminal window.
    1. python3 -m venv imbdScraper-env
    2. source imbdScraper-env/bin/activate for Mac/Linux OR source imbdScraper-env/Scripts/activate for Windows
    3. pip install -r requirements.txt
6. Once you have installed the requirements you can then run your flask app by typing in...
  - python SI507project_tools.py runserver
7. From here you'll be prompted and given a local host address. Copy this into a web
and you can then freely run the flask app. Addresses you can enter into the local
host url are as follows.
  - http://localhost:5000/


## How to use

This program is meant to be used to find movies from the IMDB top 50 that you would like to watch. It could be a big summer blockbuster, or it could be a small time foreign language film. The hope is that by giving users a comprehensive list of movies to browse, they will watch a movie that they might not have otherwise had the thought to watch.

## Routes in this application
- http://localhost:5000/
  - Homepage of the flask app, meant to introduce the system to the users.
- http://localhost:5000/search
  - Allows the user to search movies or directors within the database.
- http://localhost:5000/search_results
  - Displays the results of the search.
- http://localhost:5000/movies
  - Shows a general overview of each of the movies in the database.
- http://localhost:5000/ratings
  - Shows a general overview of the ratings for each movie in the database.

## How to run tests
1. Download all required files
2. Complete "How to run" section above"
3. Open Terminal
4. Navigate to file location of "SI507project_tests.py"
5. Make sure "SI507project_tools.py" is also there
6. Type "python SI507project_tests.py" into Terminal
7. The file will run the tests.

## In this repository:
- SI507project_tools.py
- SI507project_tests.py
- requirments.txt
- README.md
- db_diagram.jpg
- sample_movie_info.csv
- sample_movies_results.db
- sample_movies_search_cache.json
- Template file containing the HTML templates used in the Flask App.

---
## Code Requirements for Grading
Please check the requirements you have accomplished in your code as demonstrated.
- [x] This is a completed requirement.
- [ ] This is an incomplete requirement.

Below is a list of the requirements listed in the rubric for you to copy and paste.  See rubric on Canvas for more details.

### General
- [X] Project is submitted as a Github repository
- [X] Project includes a working Flask application that runs locally on a computer
- [X] Project includes at least 1 test suite file with reasonable tests in it.
- [X] Includes a `requirements.txt` file containing all required modules to run program
- [X] Includes a clear and readable README.md that follows this template
- [X] Includes a sample .sqlite/.db file
- [X] Includes a diagram of your database schema
- [X] Includes EVERY file needed in order to run the project
- [X] Includes screenshots and/or clear descriptions of what your project should look like when it is working

### Flask Application
- [X] Includes at least 3 different routes
- [X] View/s a user can see when the application runs that are understandable/legible for someone who has NOT taken this course
- [X] Interactions with a database that has at least 2 tables
- [X] At least 1 relationship between 2 tables in database
- [X] Information stored in the database is viewed or interacted with in some way

### Additional Components (at least 6 required)
- [X] Use of a new module (Pandas)
- [ ] Use of a second new module
- [ ] Object definitions using inheritance (indicate if this counts for 2 or 3 of the six requirements in a parenthetical)
- [ ] A many-to-many relationship in your database structure
- [X] At least one form in your Flask application (Search Page)
- [X] Templating in your Flask application (Everypage)
- [ ] Inclusion of JavaScript files in the application
- [X] Links in the views of Flask application page/s (Buttons located at the top of each page)
- [ ] Relevant use of `itertools` and/or `collections`
- [X] Sourcing of data using web scraping
- [ ] Sourcing of data using web REST API requests
- [ ] Sourcing of data using user input and/or a downloaded .csv or .json dataset
- [X] Caching of data you continually retrieve from the internet in some way

### Submission
- [X] I included a link to my GitHub repository with the correct permissions on Canvas! (Did you though? Did you actually? Are you sure you didn't forget?)
- [X] I included a summary of my project and how I thought it went **in my Canvas submission**!
