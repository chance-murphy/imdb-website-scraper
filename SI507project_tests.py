import sqlite3
import unittest


class HW5SQLiteDBTests(unittest.TestCase):

	def setUp(self):
		self.conn = sqlite3.connect("chocolate_sources.sqlite") # Connecting to database that should exist in autograder
		self.cur = self.conn.cursor()

	def test_for_countries_table(self):
		self.cur.execute("select countrycode, englishname, region, population, area from countries where countrycode = 'ALA'")
		data = self.cur.fetchone()
		self.assertEqual(data,('ALA', 'Åland Islands', 'Europe', 28875, 1580.0), "Testing data that results from selecting country ALA")

	def test_chocolate_insert_works(self):
		chocolate = ('A. Morin', 'Kappi', '2015', 70.0, "Haiti", 2.75)
		ch = ('A. Morin', 'Kappi', '2015', 70.0, 98, 2.75)
		self.cur.execute("insert into chocolatebars(company, specificBeanBarName, reviewDate, cocoaPercent, companyCountry, rating) values (?, ?, ?, ?, (select id from countries where englishname=?), ?)", chocolate)
		self.conn.commit()

		self.cur.execute("select company, specificBeanBarName, reviewDate, cocoaPercent, companyCountry, rating from chocolatebars where specificBeanBarName= 'Kappi'")
		data = self.cur.fetchone()
		self.assertEqual(data,ch,"Testing another select statement after a sample insertion")

	def test_for_chocolate_table(self):
		res = self.cur.execute("select * from chocolatebars")
		data = res.fetchall()
		self.assertTrue(data, 'Testing that you get a result from making a query to the chocolatebars table')

	def test_country_insert_works(self):
		country = ('SIR', '507 Islands', 'Europe', 28875, 1580.0)
		self.cur.execute("insert into countries(countrycode, englishname, region, population, area) values (?, ?, ?, ?, ?)", country)
		self.conn.commit()

		self.cur.execute("select countrycode, englishname, region, population, area from countries where countrycode = 'SIR'")
		data = self.cur.fetchone()
		self.assertEqual(data, country, "Testing a select statement where countrycode = SIR")


	def test_foreign_key_chocolate(self):
		res = self.cur.execute("select * from chocolatebars INNER JOIN countries ON chocolatebars.companyCountry = countries.id")
		data = res.fetchall()
		self.assertTrue(data, "Testing that result of selecting based on relationship between chocolatebars and countries does work")
		self.assertTrue(len(data) in [1795, 1796], "Testing that there is in fact the amount of data entered that there should have been -- based on this query of everything in both tables.{}".format(len(data)))


	def tearDown(self):
		self.conn.commit()
		self.conn.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
