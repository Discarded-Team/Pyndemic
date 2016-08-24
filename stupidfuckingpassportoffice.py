import unittest
import sqlite3
from pandemicgame import startinggame
from pandemicgame import inaturn

class T( unittest.TestCase ):

	def test_setup_sginfect (self):
		sg = startinggame ()
		sg.BoardTBL ('testboard.txt')
		sg.idTBL('testboard.txt' )
		sg.iddTBL ( )
		sg.shufid ( )
		sg.sginfect ( )
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = 'SELECT name FROM BoardTBL WHERE rcube = 1 or bcube = 1 or ycube = 1 or pcube = 1 or ucube = 1;'
			cursor.execute( tobedone)
			answerX = cursor.fetchall ( )
			answer1 = answerX [2]
			tobedone = 'SELECT name FROM BoardTBL WHERE rcube = 2 or bcube = 2 or ycube = 2 or pcube = 2 or ucube = 2;'
			cursor.execute( tobedone)
			answerY = cursor.fetchall ( )
			answer2 = answerY [2]
			tobedone = 'SELECT name FROM BoardTBL WHERE rcube = 3 or bcube = 3 or ycube = 3 or pcube = 3 or ucube = 3;'
			cursor.execute( tobedone)
			answerZ = cursor.fetchall ( )
			answer3 = answerZ [2]
		self.assertNotEqual(answer3,None,'3 countries with 3 cubes not found')
                self.assertNotEqual(answer1,None,'3 countries with 1 cubes not found')
                self.assertNotEqual(answer2,None,'3 countries with 2 cubes not found')

