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
			line1 = answer [0]
			line2 = answer [1]
			line3 = answer [2]
		print "This is the answer", answer
		print "This is line1", line1
		print "This is line2", line2
		print "This is line3", line3
		self.assertEqual(line1,'Atlanta','The table for countries was not created.')
		self.assertEqual(line2,2,'The table for countries was not created.')
		self.assertEqual(line3,'Chicago','The table for countries was not created.')

