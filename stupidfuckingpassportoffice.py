import unittest
import sqlite3
from pandemicgame import startinggame
from pandemicgame import inaturn

class T( unittest.TestCase ):

# This def tests the infect cities def.
        def test_inaturn_infectcities (self):
                it = inaturn ()
                sg = startinggame ()
                sg.BoardTBL ('testboard.txt')
                sg.idTBL('testboard.txt' )
		sg.iddTBL ()
                sg.shufid ( )
                it.infectcities (2)
                with sqlite3.connect('pandemic.db') as conn:
                        cursor = conn.cursor()
                        tobedone = """SELECT * FROM boardTBL WHERE rcube >= 1 or bcube >= 1 or ycube >= 1 or pcube >= 1 or ucube >= 1; """
                        cursor.execute( tobedone)
                        answerX = cursor.fetchall ( )
                        tobedone = """SELECT * FROM iddTBL; """
                        cursor.execute( tobedone)
                        answerY = cursor.fetchone ( )
                        answer2 = answerY [0]
                        tobedone = """SELECT rcube,bcube,ycube,ucube,pcube FROM boardTBL WHERE name is '%s';""" % (answer2)
                        cursor.execute( tobedone)
                        answerZ = cursor.fetchone ( )
			answer4a = answerZ [0]
			answer4b = answerZ [1]
			answer4c = answerZ [2]
			answer4d = answerZ [3]
			answer4e = answerZ [4]
			answer4 = answer4a + answer4b + answer4c + answer4d + answer4e
                self.assertNotEqual(answerX,None,'Something wrong')
                self.assertEqual(answer4,1,'A city card in the infection discard pile has no infection cubes on')


# This checks the character cards table has been set up.
        def test_setup_epTBL (self):
                sg = startinggame ()
                sg.BoardTBL ('testboard.txt')
                sg.pddTBL ('testboard.txt')
                sg.edTBL('testevent.txt' )
		sg.pdTBL ()
                sg.shufpd(3)
                sg.epTBL(5)
                with sqlite3.connect('pandemic.db') as conn:
                        cursor = conn.cursor()
                        tobedone = '''SELECT * FROM shufpd WHERE name = 'Ep2';'''
                        cursor.execute( tobedone)
                        answerX = cursor.fetchone ( )
                        answer1 = answerX [0]
                        answer2 = answerX [1]
		ranswer2 = int(answer2)
                self.assertEqual(answer1,'Ep2','The second epidemic card cannot be found')
                self.assertLess(ranswer2,501,'The pos of the second epidemic card is not right')
