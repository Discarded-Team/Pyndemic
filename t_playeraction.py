# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab filetype=python:

import unittest
import sqlite3
from pandemicgame import startinggame
from pandemicgame import inaturn
from pandemicgame import playeraction

# Lets a player make a direct flight from one city to another.
        def test_playeraction_direct (self):
                it = inaturn ()
                sg = startinggame ()
                sg.BoardTBL ('testboard.txt')
                sg.startinglocals (4)
                sg.player2TBL
                cards = it.gethand ('player2')
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


