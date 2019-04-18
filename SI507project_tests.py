from SI507SI507project_tools import *
import unittest
import csv
import numpy as np
import random
import itertools


class PartOne(unittest.TestCase):
    def test_movies_clean(self):
		self.cleaned_file = open('movie_info.csv','r')
        self.row_reader = self.cleaned_file.readlines()
		self.assertTrue(self.row_reader[1].split(",")[0], "Testing that there are contents in the CSV file")
		self.assertTrue(self.row_reader[50].split(",")[0], "Testing that there are 50 rows of data in the CSV File")
		self.cleaned_file.close()

	def test_movies_clean2(self):
		self.cached_file = open('movies_search_cache.json','r')
        self.row_reader = self.cleaned_file.readlines()
		self.assertTrue(self.row_reader[1].split(",")[0], "Testing that there are contents in the Cache file")
		self.cleaned_file.close()

class PartTwo(unittest.TestCase):
    def test_sample_fake_movies1(self):
        self.assertTrue(len(sample_fake_movies.split("\n")) >= 50, "Testing that there are at least 50 lines in sample_fake_movies (note that other constraints will be tested manually by humans to assure full points on this question -- deductions may still occur if instructions were not followed)")


if __name__ == "__main__":
    unittest.main(verbosity=2)
