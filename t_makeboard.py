#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

import unittest
import sqlite3
from makeboard import startinggame


class T( unittest.TestCase ):

# This def tests if a table containing a list of countries is created.
	def test_setup (self):
		sg = startinggame ()
		sg.setup ( )
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT * FROM countries;'
			cursor.execute( tobedone)
			answer = cursor.fetchone ( )
		self.assertEqual(answer,None,'The table for countries was not created.')

# This def tests that the table containging a list of countries has been created.
	def test_setupboard (self):
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
		self.assertEqual(col1,'Atlanta','The country name was not added to the database')
		self.assertEqual(col2,2,'The number of countries was not added to the database')
		self.assertEqual(col4,'Newyork','The names of connecting countries were not added to the database')

# This def tests that a research station can be found in Atlanta after game setup.
	def test_setupresearch (self):
		sg = startinggame ()
		sg.setupresearch( )
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = """SELECT research FROM countries WHERE name is 'Atlanta';"""
			cursor.execute( tobedone)
			answer = cursor.fetchone ()
		answerR = answer [0]
		self.assertEqual(answerR,1,'A research station cannot be found in Atlanta.')

# This def checks that the number of red cubs is correct
	def test_setupcubes (self):
		sg = startinggame ()
		sg.setupcubes( )
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = """SELECT nocubes FROM cubes WHERE col is 'Red';"""
			cursor.execute( tobedone)
			answer = cursor.fetchone ()
		answerR = answer [0]
		self.assertEqual(answerR,20,'The amount of Red cubes is wrong.')
	
# This def checks that the playerdeck has been created.
	def test_setupplayerdeck (self):
		sg = startinggame ()
		sg.setupplayerdeck ('testboard.txt')
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT * FROM playerdeck;'
			cursor.execute( tobedone)
			answer = cursor.fetchall ()
			col1 = answer [0]
			col2 = answer [1]
			col3 = answer [2]
		self.assertEqual(col1,'Atlanta','Player card not found')
		self.assertEqual(col2,'Chicago','Player card not found')
		self.assertEqual(col4,'Denver','Player card not found')

# This def checks that the infection cards have been shuffled into the playerdeck
	def test_setupinfect (self):
		sg = startinggame ()
		sg.setupinfect ('testboard.txt')
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT nextinfect FROM playerdeck;'
			cursor.execute( tobedone)
			answer = cursor.fetchone ()
			col1 = answer [0]
		self.assertNotEqual(col1,'NULL','No infection cards found')





#2 event cards are added per player to the player deck
#9 infection cards are drawn, and then discarded.
#3 cubes are placed on the first 3 cards drawn.
#2 cubes are placed on the next 3 cards drawn.
#1 cube is placed on the final 3 cards drawn.
#8 or 9 cards are shared between the players as starting hands
#The players are given identity cards.
#The number of epidemic cards is set (from 3-8)
#The epidemic cards are shuffled into the player deck at regular intervals.
