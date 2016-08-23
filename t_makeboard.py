import unittest
import sqlite3
from makeboard import startinggame


class T( unittest.TestCase ):

# This def tests if a table containing a list of countries is created and populated.
	def test_setup_BoardTBL (self):
		sg = startinggame ()
		sg.BoardTBL ( )
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

# This def tests that the table with the player deck cards in has been set up
	def test_setup_pdTBL (self):
		sg = startinggame ()
		sg.pdTBL ('testboard.txt')
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT name,pos FROM pdTBL;'
			cursor.execute( tobedone)
			answerX = cursor.fetchone ( )
			answer0 = answerX [0]
			answer1 = answerX [1]
		self.assertNotEqual(answer0,None,'The table for the player deck has no name column.')
		self.assertNotEqual(answer1,None,'The table for the player deck has no position in the deck column.')

# This def tests that the table with the player deck cards are discarded into has been set up
	def test_setup_pddTBL (self):
		sg = stadrtinggame ()
		sg.pddTBL ('testboard.txt')
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT name FROM pddTBL;'
			cursor.execute( tobedone)
			answerX = cursor.fetchone ( )
			answer0 = answerX [0]
		self.assertNotEqual(answer0,None,'The table for discarded player cards has no name column.')

# This def tests that the table with the infection deck has been setup.
	def test_setup_idTBL (self):
		sg = startinggame ()
		sg.idTBL( )
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT name,pos FROM idTBL;'
			cursor.execute( tobedone)
			answerX = cursor.fetchone ( )
			answer0 = answerX [0]
			answer1 = answerX [1]
		self.assertNotEqual(answer0,None,'The table for the infection deck has no name column.')
		self.assertNotEqual(answer1,None,'The table for the infection deck has no position in the deck column.')

# This def tests that the table with the infection deck has been setup.
	def test_setup_iddTBL (self):
		sg = startinggame ()
		sg.idTBL( )
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT name FROM iddTBL;'
			cursor.execute( tobedone)
			answerX = cursor.fetchone ( )
			answer0 = answerX [0]
		self.assertNotEqual(answer0,None,'The table for the infection cards to be discarded into has no name column.')

# This def tests the event deck has been setup
	def test_setup_edTBL (self):
		sg = startinggame ()
		sg.edTBL( )
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT name,pos FROM edTBL;'
			cursor.execute( tobedone)
			answerX = cursor.fetchone ( )
			answer0 = answerX [0]
			answer1 = answerX [1]
		self.assertNotEqual(answer0,None,'The table for the event cards has no name column.')
		self.assertNotEqual(answer1,None,'The table for the event cards deck has no position in the deck column.')

# This checks the character cards table has been set up.
	def test_setup_cTBL (self):
		sg = startinggame ()
		sg.cTBL( )
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT name FROM cTBL;'
			cursor.execute( tobedone)
			answerX = cursor.fetchone ( )
			answer0 = answerX [0]
			answer1 = answerX [1]
		self.assertNotEqual(answer0,None,'The table for the characters cards has no name column.')
		self.assertNotEqual(answer1,None,'The table for the characters cards deck has no position in the deck column.')

# This checks the set up of the table for the number of cubes of each colour.
	def test_setup_cubesTBL (self):
		sg = startinggame ()
		sg.cubesTBL( )
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT red,yellow,blue,black,purple FROM cubesTBL;'

			cursor.execute( tobedone)
			answerX = cursor.fetchone ( )
			answer0 = answerX [0]
			answer1 = answerX [1]
			answer2 = answerX [2]
			answer3 = answerX [3]
			answer4 = answerX [4]
		self.assertEqual(answer0,24,'The table for cubes has the wrong number of cubes in the red column.')
		self.assertEqual(answer1,24,'The table for cubes has the wrong number of cubes in the yellow column.')
		self.assertEqual(answer2,24,'The table for cubes has the wrong number of cubes in the blue column.')
		self.assertEqual(answer3,24,'The table for cubes has the wrong number of cubes in the black column.')
		self.assertEqual(answer4,24,'The table for cubes has the wrong number of cubes in the purple column.')


# This checks the set up of the table for player2's hand
	def test_setup_player2TBL (self):
		sg = startinggame ()
		sg.player2TBL( )
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT * player2TBL;'
			cursor.execute( tobedone)
			answerX = cursor.fetchone ( )
			answer0 = answerX [0]
		self.assertNotEqual(answer0,None,"""Player 2's hand has not set up properly.""")

# This checks the set up of the table for player3's hand
	def test_setup_player3TBL (self):
		sg = startinggame ()
		sg.player3TBL( )
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT * player3TBL;'
			cursor.execute( tobedone)
			answerX = cursor.fetchone ( )
			answer0 = answerX [0]
		self.assertNotEqual(answer0,None,"""Player 3's hand has not set up properly.""")

# This checks the set up of the table for player4's hand
	def test_setup_player4TBL (self):
		sg = startinggame ()
		sg.player4TBL( )
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT * player4TBL;'
			cursor.execute( tobedone)
			answerX = cursor.fetchone ( )
			answer0 = answerX [0]
		self.assertNotEqual(answer0,None,"""Player 4's hand has not set up properly.""")

# This checks the set up of the table for player1's hand
	def test_setup_player1TBL (self):
		sg = startinggame ()
		sg.player1TBL( )
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT * player1TBL;'
			cursor.execute( tobedone)
			answerX = cursor.fetchone ( )
			answer0 = answerX [0]
		self.assertNotEqual(answer0,None,"""Player 1's hand has not set up properly.""")


# This checks the character cards table has been set up.
	def test_setup_epTBL (self):
		sg = startinggame ()
		sg.epTBL( )
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT name FROM epTBL;'
			cursor.execute( tobedone)
			answerX = cursor.fetchone ( )
			answer0 = answerX [0]
			answer1 = answerX [1]
		self.assertNotEqual(answer0,None,'The table for the epidemic cards has no name column.')
		self.assertNotEqual(answer1,None,'The table for the epidemic cards cards deck has no position in the deck column.')

#9 infection cards are drawn, and then discarded.
#3 cubes are placed on the first 3 cards drawn.
#2 cubes are placed on the next 3 cards drawn.
#1 cube is placed on the final 3 cards drawn.
#8 or 9 cards are shared between the players as starting hands
#The players are given identity cards.
#The number of epidemic cards is set (from 3-8)
#The epidemic cards are shuffled into the player deck at regular intervals.
