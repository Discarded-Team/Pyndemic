# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab filetype=python:

import sqlite3
from pandemicgame import startinggame
from pandemicgame import inaturn
from pandemicgame import playeraction
it = inaturn ()
sg = startinggame ()
pa = playeraction ()

sg.startnewgame (1,'newboard.txt',1,'testevent.txt','testcharacter.txt')

