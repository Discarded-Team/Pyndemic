import unittest
import sqlite3
from pandemicgame import startinggame
from pandemicgame import inaturn

class T( unittest.TestCase ):


# This def tests the infection of the first 9 cities works right.
	def test_setup_sginfect (self):
		sg = startinggame ()
		sg.BoardTBL ('testboard.txt')
		sg.idTBL('testboard.txt' )
		sg.shufid ( )
		sg.sginfect ( )
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT * FROM boardTBL WHERE rcube > 1 ;'
			cursor.execute( tobedone)
			answerX = cursor.fetchone ( )
			answer0 = answerX [0]
			answer1 = answerX [1]
			answer2 = answerX [2]
		self.assertEqual(answer0,2,'Something wrong')
                self.assertEqual(answer1,0,'Something wrong')
                self.assertEqual(answer2,3,'Something wrong')
