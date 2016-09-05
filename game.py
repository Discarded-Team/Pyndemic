# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab filetype=python:

import sqlite3
from pandemicgame import startinggame
from pandemicgame import inaturn
from pandemicgame import playeraction
it = inaturn ()
sg = startinggame ()
pa = playeraction ()

sg.startnewgame (2,'fullboard.txt',2,'testevent.txt','testcharacter.txt')

