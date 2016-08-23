import unittest
import sqlite3
from makeboard import startinggame


class T( unittest.TestCase ):

# This def tests if a table containing a list of countries is created and populated.
	def test_setup_BoardTBL (self):
		sg = startinggame ()
		sg.BoardTBL ('testboard.txt')
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
		self.assertEqual(answer0,'Atlanta','The table for countries has no name column.')
		self.assertEqual(answer1,'u','The table for countries has no colour column.')
		self.assertEqual(answer2,2,'The table for countries has no connect column.')
		self.assertEqual(answer3,'Chicago','The table for countries has no co1 column.')
		self.assertEqual(answer4,0,'The table for countries has no co5 column.')
		self.assertEqual(answer5,0,'The table for countries has no rcube column.')
		self.assertEqual(answer6,0,'The table for countries has no bcube column.')
		self.assertEqual(answer7,0,'The table for countries has no rstation column.')

# This def tests that the table with the player deck cards in has been set up
	def test_setup_pdTBL (self):
		sg = startinggame ()
		sg.pdTBL ()
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT name,pos FROM pdTBL;'
			cursor.execute( tobedone)
			answerX = cursor.fetchone ( )
			answer0 = answerX [0]
			answer1 = answerX [1]
		self.assertEqual(answer0,'Atlanta','The table for the player deck has no name column.')
		self.assertEqual(answer1,0,'The table for the player deck has no position in the deck column.')

# This def tests that the table with the player deck cards are discarded into has been set up
	def test_setup_pddTBL (self):
		sg = startinggame ()
		sg.pddTBL ('testboard.txt')
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT name FROM pddTBL;'
			cursor.execute( tobedone)
			answerX = cursor.fetchone ( )
		self.assertEqual(answerX,None,'The table for discarded player cards has no name column.')

# This def tests that the table with the infection deck has been setup.
	def test_setup_idTBL (self):
		sg = startinggame ()
		sg.idTBL('testboard.txt' )
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT name,pos FROM idTBL;'
			cursor.execute( tobedone)
			answerX = cursor.fetchone ( )
			answer0 = answerX [0]
			answer1 = answerX [1]
		self.assertNotEqual(answer0,None,'The table for the infection deck has no name column.')
		self.assertNotEqual(answer1,None,'The table for the infection deck has no position in the deck column.')

# This def tests that the table with the infection deck discard pile has been setup.
	def test_setup_iddTBL (self):
		sg = startinggame ()
		sg.iddTBL('testboard.txt' )
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT name FROM iddTBL;'
			cursor.execute( tobedone)
			answerX = cursor.fetchone ( )
		self.assertEqual(answerX,None,'The table for the infection cards to be discarded into has no name column.')

# This def tests the event deck has been setup
	def test_setup_edTBL (self):
		sg = startinggame ()
		sg.edTBL('testevent.txt' )
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
		sg.cTBL('testcharacter.txt' )
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT name FROM cTBL;'
			cursor.execute( tobedone)
			answerX = cursor.fetchone ( )
			answer0 = answerX [0]
		self.assertEqual(answer0,'Dispatcher','The table for the characters cards has no name column.')

# This checks the set up of the table for the number of cubes of each colour.
	def test_setup_cubesTBL (self):
		sg = startinggame ()
		sg.cubesTBL( )
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT redr,yellowy,blueu,blackb,purplep FROM cubesTBL;'

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
		sg.BoardTBL ('testboard.txt')
		sg.pddTBL ('testboard.txt')
		sg.edTBL('testevent.txt' )
		sg.shuf(2)
		sg.player2TBL(2)
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT * FROM player2TBL;'
			cursor.execute(tobedone)
			answerX = cursor.fetchone ( )
			answer0 = answerX [0]
			tobedone = 'SELECT * FROM shuf ORDER BY pos ASC;'
			cursor.execute( tobedone)
			answerY = cursor.fetchone ( )
			answer1 = answerY [0]
		self.assertNotEqual(answer0,None,"""Nothing found in the hand""")
		self.assertNotEqual(answer0,answer1,"""Player 1's hand has cards still in the player deck.""")



# This checks the set up of the table for player3's hand
	def test_setup_player3TBL (self):
		sg = startinggame ()
		sg.BoardTBL ('testboard.txt')
		sg.pddTBL ('testboard.txt')
		sg.edTBL('testevent.txt' )
		sg.shuf(3)
		sg.player3TBL(3)
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT * FROM player3TBL;'
			cursor.execute(tobedone)
			answerX = cursor.fetchone ( )
			answer0 = answerX [0]
			tobedone = 'SELECT * FROM shuf ORDER BY pos ASC;'
			cursor.execute( tobedone)
			answerY = cursor.fetchone ( )
			answer1 = answerY [0]
		self.assertNotEqual(answer0,None,"""Nothing found in the hand""")
		self.assertNotEqual(answer0,answer1,"""Player 4's hand has cards still in the player deck.""")

# This checks the set up of the table for player4's hand
	def test_setup_player4TBL (self):
		sg = startinggame ()
		sg.BoardTBL ('testboard.txt')
		sg.pddTBL ('testboard.txt')
		sg.edTBL('testevent.txt' )
		sg.shuf(4)
		sg.player4TBL(4)
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT * FROM player4TBL;'
			cursor.execute(tobedone)
			answerX = cursor.fetchone ( )
			answer0 = answerX [0]
			tobedone = 'SELECT * FROM shuf ORDER BY pos ASC;'
			cursor.execute( tobedone)
			answerY = cursor.fetchone ( )
			answer1 = answerY [0]
		self.assertNotEqual(answer0,None,"""Nothing found in the hand""")
		self.assertNotEqual(answer0,answer1,"""Player 4's hand has cards still in the player deck.""")


# This checks the set up of the table for player1's hand
	def test_setup_player1TBL (self):
		sg = startinggame ()
		sg.BoardTBL ('testboard.txt')
		sg.pddTBL ('testboard.txt')
		sg.edTBL('testevent.txt' )
		sg.shuf(1)
		sg.player1TBL(1)
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT * FROM player1TBL;'
			cursor.execute(tobedone)
			answerX = cursor.fetchone ( )
			answer0 = answerX [0]
			tobedone = 'SELECT * FROM shuf ORDER BY pos ASC;'
			cursor.execute( tobedone)
			answerY = cursor.fetchone ( )
			answer1 = answerY [0]
		self.assertNotEqual(answer0,None,"""Nothing found in the hand""")
		self.assertNotEqual(answer0,answer1,"""Player 1's hand has cards still in the player deck.""")


# This checks the character cards table has been set up.
	def test_setup_epTBL (self):
		sg = startinggame ()
		sg.BoardTBL ('testboard.txt')
		sg.pddTBL ('testboard.txt')
		sg.edTBL('testevent.txt' )
		sg.shuf(3)
		sg.epTBL(5)
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT name FROM epTBL;'
			cursor.execute( tobedone)
			answerX = cursor.fetchone ( )
		self.assertNotEqual(answerX,None,'The table for the epidemic cards has no name column.')
		self.assertEqual(answerX,None,'The table for the epidemic cards cards deck has no position in the deck column.')
	
# This checks the player deck has been shuffled, without epidemic cards included.
	def test_setup_shuf (self):
		sg = startinggame ()
		sg.BoardTBL ('testboard.txt')
		sg.pddTBL ('testboard.txt')
		sg.edTBL('testevent.txt' )
		sg.shuf(3)
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT pos FROM shuf;'
			cursor.execute( tobedone)
			answerX = cursor.fetchall ( )
			answer0 = answerX [0]
			answer1 = answerX [1]
		self.assertNotEqual(answer0,0,'The deck has not shuffled correctly.')
		self.assertNotEqual(answer1,0,'The deck has not shuffled correctly.')


#9 infection cards are drawn, and then discarded.
#3 cubes are placed on the first 3 cards drawn.
#2 cubes are placed on the next 3 cards drawn.
#1 cube is placed on the final 3 cards drawn.
#8 or 9 cards are shared between the players as starting hands
#The players are given identity cards.
#The number of epidemic cards is set (from 3-8)
#The epidemic cards are shuffled into the player deck at regular intervals.
