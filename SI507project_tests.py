from SI507project_tools import *
import unittest
import csv
import json
import numpy as np
import random
import itertools


# class PartOne(unittest.TestCase):
#     # def test_movies_clean(self):
#     #     self.cleaned_file = open('movie_info.csv','r')
#     #     self.row_reader = self.cleaned_file.readlines()
#     #     self.assertTrue(self.row_reader[1].split(",")[0], "Testing that there are contents in the CSV file")
#     #     self.assertTrue(self.row_reader[50].split(",")[0], "Testing that there are 50 rows of data in the CSV File")
#     #     self.cleaned_file.close()
#
#     def setUp(self):
#         self.conn = db.connect("movies_results.db") # Connecting to database that should exist in autograder
#         self.cur = self.conn.cursor()
#
#     def test_for_movies_table(self):
#         self.cur.execute("select ReleaseDate, Director, MPAARating, RunTime from movies where Title = 'Avengers: Endgame'")
#         data = self.cur.fetchone()
#         self.assertEqual(data,('Avengers: Endgame', '(2019)', 'Anthony Russo'), "Testing data that results from selecting Avenger: Endgame")
#         self.assertTrue()

    # def test_for_ratings_table(self):
    #     self.cur.execute("select IMDBRating, Votes, Metascore from movies where Title = 'Avengers: Endgame'")
    #     data = self.cur.fetchone()
    #     self.assertEqual(data,('Avengers: Endgame', '9.2', '50,646', '78), "Testing data that results from selecting Avenger: Endgame")
    #     self.assertTrue()

class PartTwo(unittest.TestCase):
    def test_cache_file(self):
        self.cached_file = open('movies_search_cache.json','r')
        self.row_reader = self.cached_file.readlines()
        self.assertTrue(self.row_reader[0].split(",")[0], "Testing that there are contents in the Cache file")
        self.cached_file.close()

class PartThree(unittest.TestCase):
    def test_csv_file(self):
        self.csv_file = open('movie_info.csv','r')
        self.row_reader = self.csv_file.readlines()
        self.assertTrue(self.row_reader[0], "Testing that there are contents in the CSV file")
        self.csv_file.close()

class PartFour(unittest.TestCase):
    def test_csv_size(self):
        self.csv_file = open('movie_info.csv','r')
        self.row_reader = self.csv_file.readlines()
        self.assertTrue(len(self.row_reader) >= 50, "Testing that there are at least 50 lines of data in the CSV")
        self.csv_file.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
