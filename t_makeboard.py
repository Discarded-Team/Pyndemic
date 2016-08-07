#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

import unittest
import sqlite3
from makeboard import startinggame


class T( unittest.TestCase ):

# This def should test if the createcountry
	def test_setup (self):
		print "checking table created"
		sg = startinggame ()
		sg.setup ( )
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT * FROM countries;'
			cursor.execute( tobedone)
			answer = cursor.fetchone ( )
		self.assertEqual(answer,None,'The table for countries was not created.')

	def test_setupboard (self):
		print "checking table is being populated from testboard.txt"
		sg = startinggame ()
		sg.setupboard ('testboard.txt')
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT * FROM countries;'
			cursor.execute( tobedone)
			answer = cursor.fetchone ( )
			col1 = answer [0]
			col2 = answer [1]
			col4 = answer [3]
		print "This is the answer", answer
		print "This is col1", col1
		print "This is col2", col2
		print "This is col4", col4
		self.assertEqual(col1,'Atlanta','The country name was not added to the database')
		self.assertEqual(col2,2,'The number of countries was not added to the database')
		self.assertEqual(col4,'Newyork','The names of connecting countries were not added to the database')

