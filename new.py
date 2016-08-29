# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab filetype=python:

import unittest
import sqlite3
from pandemicgame import startinggame
from pandemicgame import inaturn

class T( unittest.TestCase):
        
        def test_inaturn_pdraw (self):
                it = inaturn ()
                sg = startinggame ()
                sg.startnewgameq (3,'testboard.txt',1,'testevent.txt','testcharacter.txt')
                cards1 = it.gethand ('player1')
                print cards1
                it.pdraw ('player1')
                it.pdraw ('player1')
                it.pdraw ('player1')
                cards2 = it.gethand ('player1')
                print cards2
                self.assertNotEqual(cards1,cards2,"""Player 1's hand is still the same after drawing a card """)

