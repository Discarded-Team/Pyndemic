# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab filetype=python:

import unittest
import sqlite3
from pandemicgame import startinggame
from pandemicgame import inaturn

class T( unittest.TestCase):
        
        def test_inaturn_co (self):
                it = inaturn ()
                sg = startinggame ()
                sg.startnewgameq (3,'testboard.txt',1,'testevent.txt','testcharacter.txt')
		it.epidemic ()
		it.infectcities (10)
		city01 = it.getxcube ('ucube',4)
		city02 = it.getxcube ('ycube',4)
		city03 = it.getxcube ('bcube',4)
		city04 = it.getxcube ('rcube',4)
		city05 = it.getxcube ('ucube',5)
		city06 = it.getxcube ('ycube',5)
		city07 = it.getxcube ('bcube',5)
		city08 = it.getxcube ('rcube',5)
		city09 = it.getxcube ('ucube',6)
		city10 = it.getxcube ('ycube',6)
		city11 = it.getxcube ('bcube',6)
		city12 = it.getxcube ('rcube',6)
		city13 = it.getxcube ('ucube',7)
		city14 = it.getxcube ('ycube',7)
		city15 = it.getxcube ('bcube',7)
		city16 = it.getxcube ('rcube',7)
		if city01 [0][0] >= 1:
			print "outbreak in the below"
			print city01 [1]
		if city02 [0][0] >= 1:
			print "outbreak in the below"
			print city02 [1]
		if city03 [0][0] >= 1:
			print "outbreak in the below"
			print city03 [1]
		if city04 [0][0] >= 1:
			print "outbreak in the below"
			print city04 [1]
		if city05 [0][0] >= 1:
			print "outbreak in the below"
			print city05 [1]
		if city06 [0][0] >= 1:
			print "outbreak in the below"
			print city06 [1]
		if city07 [0][0] >= 1:
			print "outbreak in the below"
			print city07 [1]
		if city08 [0][0] >= 1:
			print "outbreak in the below"
			print city08 [1]
		if city09 [0][0] >= 1:
			print "outbreak in the below"
			print city09 [1]

		print city01 + city02 + city03 + city04 + city05 + city06 + city07 + city08 + city09 + city10 + city11 + city12 + city13 + city14 + city15 + city16 
                self.assertNotEqual(cards1,cards2,"""Player 1's hand is still the same after drawing a card """)

