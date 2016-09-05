# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab filetype=python:

import unittest
import sqlite3
from pandemicgame import startinggame
from pandemicgame import inaturn
from pandemicgame import playeraction
class T( unittest.TestCase):
	it = inaturn ()
        sg = startinggame ()
	pa = playeraction ()
	sg.startnewgameq (3,'testboard.txt',1,'testevent.txt','testcharacter.txt')
# Lets a player make a direct flight from one city to another.
        def test_playeraction_direct (self):
		it = inaturn ()
	        sg = startinggame ()
		pa = playeraction ()
                cards = it.gethand ('player2')
                usecard = cards [0][0]
                if usecard != 'event1' or 'event2' or 'event3' or 'event4' or  'event5' or 'event6':
                        pa.direct ('player2',usecard)
                else:
                        usecard = cards [1][0]
                        if usecard != 'event1' or 'event2' or 'event3' or 'event4' or  'event5' or 'event6':
                                pa.direct ('player2',usecard)
                        else:
                                usecard = cards [2][0]
                                if usecard != 'event1' or 'event2' or 'event3' or 'event4' or  'event5' or 'event6':
                                        pa.direct ('player2',usecard)

                AnswerP = it.getplayer ('player2')
                self.assertEqual(AnswerP,usecard,'Player 1 has not been moved to the correct location')

	def test_playeraction_trainboat (self):
		it = inaturn ()
	        sg = startinggame ()
		pa = playeraction ()
		sg.gsTBL (3)
		player = 'player3'
		location = it.getplayer (player)
		pa.trainboat (player,location,'Chicago')
		pa.trainboat (player,'Chicago','HongKong')
		newlocation = it.getplayer (player)
		self.assertEqual(newlocation,'HongKong','Player 3 has not been moved to HongKong as expected')
