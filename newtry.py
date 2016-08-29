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
                it.co ()
                outbreaks = it.getoc ()
                self.assertNotEqual(outbreaks,0,"""At least 1 outbreak should have happend. Counter still at zero!""")
# it.getxcube ('ucube',4)
 
