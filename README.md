# Chance Murphy 507 Final Project

Chance Murphy

[Link to this repository](https://github.com/chance-murphy/si-507-final-project)

---

## Project Description

As of now this program scrapes the IMDB page https://www.imdb.com/search/title?title_type=feature,&num_votes=1000,&languages=en&sort=user_rating,desc and gives me the data for the movie title, release date, run time, MPAA rating, IMDB rating, and Metascore. I still need to successfully scrape the data for the director and box office total. Director is proving to be tricky because it is located inside of <p> tag with no class while box office total is proving to be tricky because it is located in a <span> tag that also contains the total votes it has received on IMDB. The search URL is cached in my cache diction so that if a search is repeated I won't make multiple requests for the same data.

I still need to...
- Clean the data
- Upload the cleaned data to a CSV (This is all set up, the data just needs to be cleaned first)
- Upload the data to my db tables
- Create app routes to display data to the user
- Set up HTML template so that I can base search based on user input
- Figure out how to edit the URL so that user input can be used in the scrape (I have a pretty good idea of how to do this, it's a matter of trial and error at this point)

## How to run

1. ...

## How to use

1. ...

## Routes in this application
- Undecided as of now

## How to run tests
1. Undecided as of now

## In this repository:
- SI507project_tools.py
- SI507project_tests.py
- README.md

---
## Code Requirements for Grading
Please check the requirements you have accomplished in your code as demonstrated.
- [x] This is a completed requirement.
- [ ] This is an incomplete requirement.

Below is a list of the requirements listed in the rubric for you to copy and paste.  See rubric on Canvas for more details.

### General
- [X] Project is submitted as a Github repository
- [ ] Project includes a working Flask application that runs locally on a computer
- [ ] Project includes at least 1 test suite file with reasonable tests in it.
- [ ] Includes a `requirements.txt` file containing all required modules to run program
- [X] Includes a clear and readable README.md that follows this template
- [ ] Includes a sample .sqlite/.db file
- [X] Includes a diagram of your database schema
- [X] Includes EVERY file needed in order to run the project
- [ ] Includes screenshots and/or clear descriptions of what your project should look like when it is working

### Flask Application
- [ ] Includes at least 3 different routes
- [ ] View/s a user can see when the application runs that are understandable/legible for someone who has NOT taken this course
- [ ] Interactions with a database that has at least 2 tables
- [ ] At least 1 relationship between 2 tables in database
- [ ] Information stored in the database is viewed or interacted with in some way

### Additional Components (at least 6 required)
- [ ] Use of a new module
- [ ] Use of a second new module
- [ ] Object definitions using inheritance (indicate if this counts for 2 or 3 of the six requirements in a parenthetical)
- [ ] A many-to-many relationship in your database structure
- [ ] At least one form in your Flask application
- [ ] Templating in your Flask application
- [ ] Inclusion of JavaScript files in the application
- [ ] Links in the views of Flask application page/s
- [ ] Relevant use of `itertools` and/or `collections`
- [X] Sourcing of data using web scraping
- [ ] Sourcing of data using web REST API requests
- [ ] Sourcing of data using user input and/or a downloaded .csv or .json dataset
- [X] Caching of data you continually retrieve from the internet in some way

### Submission
- [X] I included a link to my GitHub repository with the correct permissions on Canvas! (Did you though? Did you actually? Are you sure you didn't forget?)
- [ ] I included a summary of my project and how I thought it went **in my Canvas submission**!
