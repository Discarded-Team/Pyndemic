import unittest
import sqlite3
from makeboard import startinggame


class T( unittest.TestCase ):


# This def tests that the table with the game state has been setup.
	def test_setup_gsTBL (self):
		sg = startinggame ()
		sg.gsTBL(3)
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT ir,oc,players FROM gsTBL;'
			cursor.execute( tobedone)
			answerX = cursor.fetchone ( )
			answer0 = answerX [0]
			answer1 = answerX [1]
			answer2 = answerX [2]
		self.assertEqual(answer0,2,'The infection rate is not two. It should be at the start of the game.')
                self.assertEqual(answer1,0,'The number of outbreaks is not 0. It should be.')
                self.assertEqual(answer2,3,'The number of players is not 3. It should be.')
