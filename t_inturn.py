# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab filetype=python:

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
                sg.idTBL ()
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

# Tests the "get location of a given player def"		
	def test_inaturn_getplayer (self):
		it = inaturn ()
                sg = startinggame ()
                sg.BoardTBL ('testboard.txt')
		sg.startinglocals (4)
		answerA = it.getplayer ('notplayer')
		answerB = it.getplayer ('player2')
		answerC = it.getplayer ('player4')
                self.assertEqual(answerB,'Atlanta','Something wrong with the info!')
                self.assertEqual(answerC,'Atlanta','Something wrong with the info!')
                self.assertEqual(answerA,'There is no player of that name!','This will not handle requests where player name is wrong')

# Tests the "get discarded infection deck cards"
	def test_inaturn_getidd (self):
		it = inaturn ()
                sg = startinggame ()
                sg.BordTBL ('testboard.txt')
		sg.idTBL ( )
		sg.iddTBL ()
		sg.infectcities (3)
		answerD = it.getidd ()
                self.assertNotEqual(answerD,None,'No cards found in the infection deck discard pile')

# Gives the cards in a given players hand
	def test_inaturn_gethand (self):
		it = inaturn ()
                sg = startinggame ()
                sg.BordTBL ('testboard.txt')
		sg.pddTBL ()
                sg.edTBL('testevent.txt' )
                sg.shufpd(2)
		sg.player1TBL (2)
		answerE = it.gethand ('player1')
                self.assertNotEqual(answerE,None,"""No cards found in player 1's hand""")

# Gives the cubes of a given colour remaining
	def test_inaturn_getcubes (self):
		it = inaturn ()
                sg = startinggame ()
                sg.BordTBL ('testboard.txt')
		sg.idTBL ()
		sg.iddTBL ()
		it.infectcities (7)
		AnswerF = it.getcubes (rcubes)
		AnswerG = it.getcubes (ycubes)
		AnswerH = it.getcubes (pcubes)
		AnswerI = it.getcubes (bcubes)
		AnswerJ = it.getcubes (ucubes)
		AnswerK =  AnswerF + AnswerG + AnswerH + AnswerI + AnswerJ
                self.assertNotEqual(AnswerF,None,"""Answer given for Red cubes""")
                self.assertNotEqual(AnswerG,None,"""Answer given for Yellow cubes""")
                self.assertNotEqual(AnswerH,None,"""Answer given for Purple cubes""")
                self.assertNotEqual(AnswerI,None,"""Answer given for Black cubes""")
                self.assertNotEqual(AnswerJ,None,"""Answer given for Blue cubes""")
                self.assertEqual(AnswerK,7,"""Should be 7 disease cubes, but can't find them.""")
		

# Gives the infection rate
	def test_inaturn_getir (self):
		it = inaturn ()
                sg = startinggame ()
		sg.gsTBL (3)
		AnswerL = it.getir ( )
		self.assertEqual(AnswerL,2, """Infection rate cant be found or isn't 2""")


# Gives the number of outbreaks
	def test_inaturn_getir (self):
		it = inaturn ()
                sg = startinggame ()
		sg.gsTBL (3)
		AnswerM = it.getor ( )
		self.assertEqual(AnswerM,0, """Outbreak count cant be found or isn't 0""")

# Returns all cities with X cubes in
	def test_inaturn_getxcube (self):
		it = inaturn ()
                sg = startinggame ()
                sg.BordTBL ('testboard.txt')
		sg.idTBL ( )
		sg.iddTBL ()
		sg.infect ()
		AnswerN = it.getcube (2)
                self.assertNotEqual(AnswerN,None,'No cities with two cubes of a given colour in can be found')

# Moves a given player from a given city to another given city
	def test_inaturn_move (self):
		it = inaturn ()
		sg = startinggame ()
		sg.BoardTBL ('testboard.txt')
		sg.startinglocals (4)
		it.move ('player1', 'Atlanta', 'Chicago')
		AnswerO = it.getplayer ('player1')
		print AnswerO
                self.assertEqual(AnswerO,'Chicago','Player 1 has not been moved to Chicago')

# Lets a player make a direct flight from one city to another.
	def test_inaturn_direct (self):
		it = inaturn ()
                sg = startinggame ()
                sg.BordTBL ('testboard.txt')
		sg.startinglocals (4)
		sg.player2TBL
		cards =	it.gethand ('player2')
		usecard = cards [0]
		if usecard != 'event1' or 'event2' or 'event3' or 'event4' or  'event5' or 'event6':
			it.direct (usecard)
		else:
			usecard = cards [1]
			if usecard != 'event1' or 'event2' or 'event3' or 'event4' or  'event5' or 'event6':
				it.direct (usecard)
			else:
				usecard = cards [1]
				if usecard != 'event1' or 'event2' or 'event3' or 'event4' or  'event5' or 'event6':
					it.direct (usecard)
			
		AnswerP = it.getplayer ('player1')
                self.assertEqual(AnswerP,usecard,'Player 1 has not been moved to the correct location')

#- direct flight discarding the card of the destination city
#- charter flight discarding card from the departure city
#- shuttle flight from one research station to another
#- treat disease
#- cure disease
#- share knowledge
#- build a research station 

# Tests the "get discarded player deck cards"
