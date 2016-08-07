#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

import unittest
import sqlite3
from makeboard import startinggame


class T( unittest.TestCase ):

# This def should test if the createcountry
	def test_setup (self):
		sg = startinggame ()
		sg.setup ( )
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT * FROM countries;'
			cursor.execute( tobedone)
			answer = cursor.fetchone ( )
		print "This is the answer", answer
		self.assertEqual(answer,None,'The table for countries was not created.')

	def test_setupboard (self):
		sg = startinggame ()
		sg.setupboard ('testboard.txt')
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT * FROM countries;'
			cursor.execute( tobedone)
			answer = cursor.fetchone ( )
			line1 = answer [0]
		print "This is the answer", answer
		print "This is line1", line1
		self.assertEqual(Line1,'Atlanta,2,Newyork,Chiago','The table for countries was not created.')

