#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

import unittest
import sqlite3
from makeboard import startinggame


class T( unittest.TestCase ):

# This def tests if a table containing a list of countries is created and populated.
        def test_setup (self):
                sg = startinggame ()
                sg.setup ( )
                with sqlite3.connect('pandemic.db') as conn:
                        cursor = conn.cursor()
                        tobedone = 'SELECT name, colour, connect, co1, co5, rcube, bcube, rstation FROM BoardTBL;'
                        cursor.execute( tobedone)
                        answerX = cursor.fetchone ( )
                        answer0 = answerX [0]
                        answer1 = answerX [1]
                        answer2 = answerX [2]
                        answer3 = answerX [3]
                        answer4 = answerX [4]
                        answer5 = answerX [5]
                        answer6 = answerX [6]
                        answer7 = answerX [7]
                self.assertNotEqual(answer0,None,'The table for countries has no name column.')
                self.assertNotEqual(answer1,None,'The table for countries has no colour column.')
                self.assertNotEqual(answer2,None,'The table for countries has no connect column.')
                self.assertNotEqual(answer3,None,'The table for countries has no co1 column.')
                self.assertNotEqual(answer4,None,'The table for countries has no co5 column.')
                self.assertNotEqual(answer5,None,'The table for countries has no rcube column.')
                self.assertNotEqual(answer6,None,'The table for countries has no bcube column.')
                self.assertNotEqual(answer7,None,'The table for countries has no rstation column.')

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

# This def checks event cards have been added
	def test_setupevent (self):
		sg = startinggame ()
		sg.setupevent ('testboard.txt')
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT nextevent FROM playerdeck;'
			cursor.execute( tobedone)
			answer = cursor.fetchone ()
			col1 = answer [0]
		self.assertNotEqual(col1,'NULL','No event cards found')


	def test_setupinfectcities (self):
		sg = startinggame ()
		sg.setupinfectcities ('testboard.txt')
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = """SELECT bcube FROM countries WHERE name is 'Atlanta';"""
			cursor.execute( tobedone)
			answer = cursor.fetchone ()
			col1 = answer [0]
			tobedone = """SELECT bcube FROM countries WHERE bcube = 3;"""
			cursor.execute( tobedone)
			answer = cursor.fetchone ()
			col2 = answer [0]
			tobedone = """SELECT name FROM discard;"""
			cursor.execute( tobedone)
			answer = cursor.fetchone ()
			col3 = answer [0]
		self.assertNotEqual(col1,'NULL','No cube column for Atlanta')
		self.assertNotEqual(col2,'NULL','No places with 3 cubes found')
		self.assertEqual(col3,'NULL','discard pile cannot be found')

#9 infection cards are drawn, and then discarded.
#3 cubes are placed on the first 3 cards drawn.
#2 cubes are placed on the next 3 cards drawn.
#1 cube is placed on the final 3 cards drawn.
#8 or 9 cards are shared between the players as starting hands
#The players are given identity cards.
#The number of epidemic cards is set (from 3-8)
#The epidemic cards are shuffled into the player deck at regular intervals.
