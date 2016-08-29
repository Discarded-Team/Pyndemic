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
	def test_inaturn_getcitycubes (self):
		it = inaturn ()
                sg = startinggame ()
                sg.BoardTBL ('testboard.txt')
		answerZ = it.getcitycubes ('ucube','notacity')
		answerX = it.getcitycubes ('ucube','Atlanta')
                self.assertEqual(answerX,0,'Something wrong with the info!')
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

# Tests the "get discarded player deck cards"
	def test_inaturn_getpdd (self):
		it = inaturn ()
                sg = startinggame ()
                sg.BoardTBL ('testboard.txt')
		sg.pdTBL ( )
		sg.pddTBL ()
		answerD = it.getpdd ()
                self.assertNotEqual(answerD,None,'No cards found in the player deck discard pile')

# Gives the cards in a given players hand
	def test_inaturn_gethand (self):
		it = inaturn ()
                sg = startinggame ()
                sg.BoardTBL ('testboard.txt')
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
		sg.cubesTBL ()
                sg.BoardTBL ('testboard.txt')
		sg.idTBL ()
		sg.iddTBL ()
		it.infectcities (7)
		AnswerF = it.getcubes ('rcube')
		AnswerG = it.getcubes ('ycube')
		AnswerH = it.getcubes ('pcube')
		AnswerI = it.getcubes ('bcube')
		AnswerJ = it.getcubes ('ucube')
		AnswerK =  AnswerF + AnswerG + AnswerH + AnswerI + AnswerJ
                self.assertNotEqual(AnswerF,None,"""Answer given for Red cubes""")
                self.assertNotEqual(AnswerG,None,"""Answer given for Yellow cubes""")
                self.assertNotEqual(AnswerH,None,"""Answer given for Purple cubes""")
                self.assertNotEqual(AnswerI,None,"""Answer given for Black cubes""")
                self.assertNotEqual(AnswerJ,None,"""Answer given for Blue cubes""")
                self.assertEqual(AnswerK,101,"""Should be 101 disease cubes left, but can't find them.""")
		

# Gives the infection rate
	def test_inaturn_getir (self):
		it = inaturn ()
                sg = startinggame ()
		sg.gsTBL (3)
		AnswerL = it.getir ( )
		self.assertEqual(AnswerL,2, """Infection rate cant be found or isn't 2""")


# Gives the number of outbreaks
	def test_inaturn_getoc (self):
		it = inaturn ()
                sg = startinggame ()
		sg.gsTBL (3)
		AnswerM = it.getoc ( )
		self.assertEqual(AnswerM,0, """Outbreak count cant be found or isn't 0""")

# Returns the number and names of all cities with X cubes of a given colour
	def test_inaturn_getxcube (self):
		it = inaturn ()
                sg = startinggame ()
                sg.BoardTBL ('testboard.txt')
                sg.idTBL( )
                sg.iddTBL ( )
                sg.shufid ( )
                sg.sginfect ( )
		AnswerN1 = it.getxcube ('ucube',2)
		AnswerN2 = it.getxcube ('bcube',2)
		AnswerN3 = it.getxcube ('ycube',2)
		AnswerN4 = it.getxcube ('rcube',2)
		AnswerN11 = AnswerN1 [0][0]
		AnswerN21 = AnswerN2 [0][0]
		AnswerN31 = AnswerN3 [0][0]
		AnswerN41 = AnswerN4 [0][0]
		AnswerN5 = AnswerN11 + AnswerN21 + AnswerN31 + AnswerN41
                self.assertNotEqual(AnswerN1,None,'No cities with two cubes of a given colour in can be searched for')
                self.assertNotEqual(AnswerN2,None,'No cities with two cubes of a given colour in can be searched for')
                self.assertNotEqual(AnswerN3,None,'No cities with two cubes of a given colour in can be searched for')
                self.assertNotEqual(AnswerN4,None,'No cities with two cubes of a given colour in can be searched for')
                self.assertEqual(AnswerN5,3,'The correct number of cities with 2 cubes in cannot be found')

# Moves a given player from a given city to another given city
	def test_inaturn_move (self):
		it = inaturn ()
		sg = startinggame ()
		sg.BoardTBL ('testboard.txt')
		sg.startinglocals (4)
		it.move ('player1', 'Atlanta', 'Chicago')
		AnswerO = it.getplayer ('player1')
                self.assertEqual(AnswerO,'Chicago','Player 1 has not been moved to Chicago')


# This def gives all cubes of each colour for a given city
	def test_inaturn_getcityallcubes (self):
		print "needs fixing"
		it = inaturn ()
                sg = startinggame ()
                sg.BoardTBL ('testboard.txt')
		answerZ = it.getcityallcubes ('notacity')
		answerX = it.getcityallcubes ('Atlanta')
#                self.assertEqual(answerX,'There are 0 blue cubes, 0 black cubes, 0 red cubes, 0 yellow cubes and 0 purple cubes in Atlanta.')
                self.assertEqual(answerZ,'There is no city of that name!','This will not handle requests where city name is wrong')

# This def reduces the number of cubes of a given colour by 1
	def test_inaturn_usecube (self):
		it = inaturn ()
                sg = startinggame ()
		sg.cubesTBL ()
		it.usecube ('ucube')
                with sqlite3.connect('pandemic.db') as conn:
                        cursor = conn.cursor()
                        tobedone = """SELECT ucube FROM cubesTBL; """
                        cursor.execute( tobedone)
			Answer = cursor.fetchone ()
		AnswerQ = Answer [0]
                self.assertEqual(AnswerQ,23,'The number of cubes has not been reduced by 1 to 23.')
			

# Tests the "get discarded infection deck cards"
	def test_inaturn_getidd (self):
		it = inaturn ()
                sg = startinggame ()
                sg.BoardTBL ('testboard.txt')
		sg.idTBL ( )
		sg.iddTBL ()
		sg.shufid ()
		it.infectcities (3)
		answerD = it.getidd ()
                self.assertNotEqual(answerD,None,'No cards found in the infection deck discard pile')



	def test_inaturn_discard (self):
		it = inaturn ()
                sg = startinggame ()
                sg.BoardTBL ('testboard.txt')
		sg.pdTBL ( )
		sg.pddTBL ()
		sg.shufid ()
		sg.player1TBL (4)
		cards = it.gethand ('player1')
		thing = cards [0]
		todiscard = thing [0]
		it.discard ('player1',todiscard)
                with sqlite3.connect('pandemic.db') as conn:
                        cursor = conn.cursor()
                        tobedone = """SELECT name FROM pddTBL WHERE name is '%s'; """ % (todiscard)
                        cursor.execute( tobedone)
			Answer = cursor.fetchone ()
		AnswerZ = Answer [0]
		cards = it.gethand ('player1')
		inhand = cards [0]
                self.assertEqual(AnswerZ,todiscard,'Discarded card not found in discard pile')
                self.assertNotEqual(AnswerZ,inhand,'Discarded card found in players hand!')
		
			
		
	
	def test_inaturn_pdraw (self):	
		it = inaturn ()
                sg = startinggame ()
                sg.startnewgameq (3,'testboard.txt',1,'testevent.txt','testcharacter.txt')
		cards1 = it.gethand ('player1')
		it.pdraw ('player1')
		it.pdraw ('player1')
		it.pdraw ('player1')
		cards2 = it.gethand ('player1')
                self.assertNotEqual(cards1,cards2,"""Player 1's hand is still the same after drawing a card """)

	def test_inaturn_epidemic (self):
		it = inaturn ()
		sg = startinggame ()
		sg.startnewgameq (2,'testboard.txt',6,'testevent.txt','testcharacter.txt')
		it.infectcities (4)
		eps = 0
		problem = 0
		while problem < 20:
			with sqlite3.connect('pandemic.db') as conn:
				cursor = conn.cursor()
	                        tobedone = """SELECT ec FROM gsTBL; """
       		                cursor.execute( tobedone)
				Answer = cursor.fetchone ()
				eps = Answer [0]
				if eps == 1:
					break
				it.pdraw ('player1')
				problem = problem + 1
		AnswerF = it.getcubes ('rcube')
		AnswerG = it.getcubes ('ycube')
		AnswerH = it.getcubes ('pcube')
		AnswerI = it.getcubes ('bcube')
		AnswerJ = it.getcubes ('ucube')
		AnswerE1 = it.getxcube ('ucube',3)
		AnswerE2 = it.getxcube ('bcube',3)
		AnswerE3 = it.getxcube ('rcube',3)
		AnswerE4 = it.getxcube ('ycube',3)
		AnswerE11 = AnswerE1 [0][0]
		AnswerE21 = AnswerE2 [0][0]
		AnswerE31 = AnswerE3 [0][0]
		AnswerE41 = AnswerE4 [0][0]
 		AnswerE5 = AnswerE11 + AnswerE21 + AnswerE31 + AnswerE41
		AnswerK =  AnswerF + AnswerG + AnswerH + AnswerI + AnswerJ
                self.assertEqual(eps,1,"""An epidemic hasn't happened""")
                self.assertEqual(AnswerK,83,"""Should be 83 disease cubes left, but can't find them.""")
                self.assertEqual(AnswerE5,4,"""4 cities cannot be found with 3 cubes on, which isn't right.""")

        def test_inaturn_ic (self):
                it = inaturn ()
                sg = startinggame ()
                sg.BoardTBL ('testboard.txt')
                sg.idTBL ()
                sg.iddTBL ()
                sg.shufid ( )
                it.ic ('u','Bogota')
                it.ic ('y','Atlanta')
                it.ic ('y','Atlanta')
                Answer1 = it.getcitycubes ('ucube','Bogota')
                Answer2 = it.getcitycubes ('ycube','Atlanta')
                self.assertEqual(Answer1,1,"""Bogota should have a single blue cube in now. It does not""")
                self.assertEqual(Answer2,2,"""Atlanta should have two yellow cubes in now. It does not""")
	

	def test_inaturn_co (self):
                it = inaturn ()
                sg = startinggame ()
                sg.startnewgameq (3,'testboard.txt',1,'testevent.txt','testcharacter.txt')
                it.epidemic ()
                it.infectcities (10)
                it.co ()
                outbreaks = it.getoc ()
                self.assertNotEqual(outbreaks,0,"""At least 1 outbreak should have happend. Counter still at zero!""")
# it.getxcube ('ucube',4)
 
	
