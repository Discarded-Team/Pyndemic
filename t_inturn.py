import unittest
import sqlite3
from pandemicgame import startinggame
from pandemicgame import inaturn

class T( unittest.TestCase):
# this def tests the infect cities def.
        def test_inaturn_infectcities (self):
                it = inaturn ()
                sg = startinggame ()
                sg.BoardTBL ('testboard.txt')
                sg.idTBL()
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

# this def tests the how many cubes in a city command
	def test_inaturn_getcubes (self):
		it = inaturn ()
                sg = startinggame ()
                sg.BoardTBL ('testboard.txt')
		answerZ = it.getcubes ('notacity')
		answerX = it.getcubes ('Atlanta')
                self.assertEqual(answerX,'There are 0 blue cubes, 0 black cubes, 0 red cubes, 0 yellow cubes and  0 purple cubes in Atlanta.','Something wrong with the info!')
                self.assertEqual(answerZ,'There is no city of that name!','This will not handle requests where city name is wrong')
		
	def test_inaturn_getplayer (self):
		it = inaturn ()
                sg = startinggame ()
                sg.BoardTBL ('testboard.txt')
		sg.startinglocals (2)
		answerA = it.getplayer ('notplayer')
		answerB = it.getplayer ('player2')
		print answerA
		print answerB
                self.assertEqual(answerB,'player2 is located in Atlanta','Something wrong with the info!')
                self.assertEqual(answerA,'There is no player of that name!','This will not handle requests where player name is wrong')
#- How many cubes in city X
#- Location of player X
#- Cards in idd
#- Cards in pdd
#- Cards in player X hand
#- Cubes of colour X remaining
#- Infection rate
#- Number of outbreaks
