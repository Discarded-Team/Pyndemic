#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

import sqlite3
import random

# This creates and populates the table which contains the information from the game board.
class startinggame:
	def startinglocals (self,players):
		with sqlite3.connect('pandemic.db') as conn:
		       	cursor = conn.cursor()
	            	tobedone = """UPDATE BoardTBL set rstation = 1 WHERE name is 'Atlanta';"""
	            	cursor.execute( tobedone )
			if players == 1:
	            		tobedone = """UPDATE BoardTBL set player1 = 1 WHERE name is 'Atlanta';"""
		            	cursor.execute( tobedone )
			if players == 2:
	            		tobedone = """UPDATE BoardTBL set player1 = 1 WHERE name is 'Atlanta';"""
		            	cursor.execute( tobedone )
	            		tobedone = """UPDATE BoardTBL set player2 = 1 WHERE name is 'Atlanta';"""
		            	cursor.execute( tobedone )
			if players == 3:
	            		tobedone = """UPDATE BoardTBL set player2 = 1 WHERE name is 'Atlanta';"""
		            	cursor.execute( tobedone )
	            		tobedone = """UPDATE BoardTBL set player1 = 1 WHERE name is 'Atlanta';"""
		            	cursor.execute( tobedone )
	            		tobedone = """UPDATE BoardTBL set player3 = 1 WHERE name is 'Atlanta';"""
		            	cursor.execute( tobedone )
			if players == 4:
	            		tobedone = """UPDATE BoardTBL set player2 = 1 WHERE name is 'Atlanta';"""
		            	cursor.execute( tobedone )
	            		tobedone = """UPDATE BoardTBL set player1 = 1 WHERE name is 'Atlanta';"""
		            	cursor.execute( tobedone )
	            		tobedone = """UPDATE BoardTBL set player3 = 1 WHERE name is 'Atlanta';"""
		            	cursor.execute( tobedone )
	            		tobedone = """UPDATE BoardTBL set player4 = 1 WHERE name is 'Atlanta';"""
		            	cursor.execute( tobedone )
			conn.commit()


	def BoardTBL (self,board):
		with sqlite3.connect('pandemic.db') as conn:
	            	cursor = conn.cursor()
	            	tobedone = 'DROP TABLE if exists BoardTBL;'
	            	cursor.execute( tobedone )
			conn.commit()
			tobedone = '''CREATE TABLE BoardTBL(
			"name",
			"colour",
			"connect",
			"co1",
			"co2",
			"co3",		
			"co4",
			"co5",
			"co6",
			"rcube",
			"ycube",
			"bcube",
			"ucube",
			"pcube",
			"rstation",
			"player1",
			"player2",
			"player3",
			"player4");'''
			cursor.execute( tobedone )
			conn.commit()
			boardfile = open(board,'r') 
			for line in boardfile:
				with sqlite3.connect('pandemic.db') as conn:
			        	cursor = conn.cursor()
		            		tobedone = """INSERT INTO BoardTBL (name,
			colour,
			connect,
			co1,
			co2,
			co3,		
			co4,
			co5,
			co6,
			rcube,
			ycube,
			bcube,
			ucube,
			pcube,
			rstation,
			player1,
			player2,
			player3,
			player4) VALUES (%s);""" % (line)
		            		cursor.execute( tobedone )
					conn.commit()

# This sets up the player deck and populates it
	def pdTBL (self):
		with sqlite3.connect('pandemic.db') as conn:
	            	cursor = conn.cursor()
	            	tobedone = 'DROP TABLE if exists pdTBL;'
	            	cursor.execute( tobedone )
			conn.commit()
			tobedone = '''CREATE TABLE pdTBL(
			"name",
			"pos");'''
			cursor.execute( tobedone )
			conn.commit()
		        tobedone = """INSERT INTO pdTBL (name) select name from BoardTBL;""" 
	 		cursor.execute( tobedone )
			conn.commit()
	       		tobedone = """UPDATE pdTBL SET pos = 0;""" 
	       		cursor.execute( tobedone )
			conn.commit()

# This sets up the player deck discard pile
	def pddTBL (self):
		with sqlite3.connect('pandemic.db') as conn:
	            	cursor = conn.cursor()
	            	tobedone = 'DROP TABLE if exists pddTBL;'
	            	cursor.execute( tobedone )
			conn.commit()
			tobedone = '''CREATE TABLE pddTBL(
			"name");'''
			cursor.execute( tobedone )
			conn.commit()

# This sets up the infection deck and populates it
	def idTBL (self):
		with sqlite3.connect('pandemic.db') as conn:
	            	cursor = conn.cursor()
	            	tobedone = 'DROP TABLE if exists idTBL;'
	            	cursor.execute( tobedone )
			conn.commit()
			tobedone = '''CREATE TABLE idTBL(
			"name",
			"pos");'''
			cursor.execute( tobedone )
			conn.commit()
		        tobedone = """INSERT INTO idTBL (name) select name from BoardTBL;""" 
		        cursor.execute( tobedone )
			conn.commit()
		        tobedone = """UPDATE idTBL SET pos = 0;""" 
		        cursor.execute( tobedone )
			conn.commit()

# This sets up the infection deck discard pile
	def iddTBL (self):
		with sqlite3.connect('pandemic.db') as conn:
	            	cursor = conn.cursor()
	            	tobedone = 'DROP TABLE if exists iddTBL;'
	            	cursor.execute( tobedone )
			conn.commit()
			tobedone = '''CREATE TABLE iddTBL(
			"name");'''
			cursor.execute( tobedone )
			conn.commit(



)

# This sets up the event deck and populates it
	def edTBL (self,event):
		with sqlite3.connect('pandemic.db') as conn:
	            	cursor = conn.cursor()
	            	tobedone = 'DROP TABLE if exists edTBL;'
	            	cursor.execute( tobedone )
			conn.commit()
			tobedone = '''CREATE TABLE edTBL(
			"name",
			"pos");'''
			cursor.execute( tobedone )
			conn.commit()
			eventfile = open(event,'r') 
			for line in eventfile:
				with sqlite3.connect('pandemic.db') as conn:
		            		tobedone = """INSERT INTO edTBL (name,pos) VALUES (%s);""" % (line)
		            		cursor.execute( tobedone )
					conn.commit()
			tobedone = '''UPDATE edTBL SET pos = ABS(RANDOM() % 500);'''
			cursor.execute( tobedone )
			conn.commit()

# This sets up the character deck and populates it
	def cTBL (self,character):
		with sqlite3.connect('pandemic.db') as conn:
	            	cursor = conn.cursor()
	            	tobedone = 'DROP TABLE if exists cTBL;'
	            	cursor.execute( tobedone )
			conn.commit()
			tobedone = '''CREATE TABLE cTBL(
			"name",
			"pos",
			"player");'''
			cursor.execute( tobedone )
			conn.commit()
			eventfile = open(character,'r') 
			for line in eventfile:
				with sqlite3.connect('pandemic.db') as conn:
		            		tobedone = """INSERT INTO cTBL (name,pos) VALUES (%s);""" % (line)
		            		cursor.execute( tobedone )
					conn.commit()
			tobedone = '''UPDATE cTBL SET pos = ABS(RANDOM() % 500);'''
			cursor.execute( tobedone )
			conn.commit()

# This gives each player an identity
	def caTBL (self):
		with sqlite3.connect('pandemic.db') as conn:
	            	cursor = conn.cursor()
	            	tobedone = """SELECT name FROM cTBL ORDER BY pos ASC limit 1;"""
	            	cursor.execute( tobedone )
			answerX = cursor.fetchone ()
			answer1 = answerX [0]
			tobedone = '''UPDATE cTBL SET player = 'player1' WHERE name is '%s' ''' % (answer1)
			cursor.execute( tobedone )
			conn.commit()
			tobedone = '''UPDATE cTBL SET pos = 600 WHERE name is '%s' ''' % (answer1)
			cursor.execute( tobedone )
			conn.commit()
	            	tobedone = """SELECT name FROM cTBL ORDER BY pos ASC limit 1;"""
	            	cursor.execute( tobedone )
			answerX = cursor.fetchone ()
			answer1 = answerX [0]
			tobedone = '''UPDATE cTBL SET player = 'player2' WHERE name is '%s' ''' % (answer1)
			cursor.execute( tobedone )
			conn.commit()
			tobedone = '''UPDATE cTBL SET pos = 600 WHERE name is '%s' ''' % (answer1)
			cursor.execute( tobedone )
			conn.commit()
	            	tobedone = """SELECT name FROM cTBL ORDER BY pos ASC limit 1;"""
	            	cursor.execute( tobedone )
			answerX = cursor.fetchone ()
			answer1 = answerX [0]
			tobedone = '''UPDATE cTBL SET player = 'player3' WHERE name is '%s' ''' % (answer1)
			cursor.execute( tobedone )
			conn.commit()
			tobedone = '''UPDATE cTBL SET pos = 600 WHERE name is '%s' ''' % (answer1)
			cursor.execute( tobedone )
			conn.commit()
	            	tobedone = """SELECT name FROM cTBL ORDER BY pos ASC limit 1;"""
	            	cursor.execute( tobedone )
			answerX = cursor.fetchone ()
			answer1 = answerX [0]
			tobedone = '''UPDATE cTBL SET player = 'player4' WHERE name is '%s' ''' % (answer1)
			cursor.execute( tobedone )
			conn.commit()
			tobedone = '''UPDATE cTBL SET pos = 600 WHERE name is '%s' ''' % (answer1)
			cursor.execute( tobedone )
			conn.commit()
			
		



# This sets up the table of disease cubes
	def cubesTBL (self):
		with sqlite3.connect('pandemic.db') as conn:
	            	cursor = conn.cursor()
	            	tobedone = 'DROP TABLE if exists cubesTBL;'
	            	cursor.execute( tobedone )
			conn.commit()
			tobedone = '''CREATE TABLE cubesTBL(
			"redr",
			"yellowy",
			"blackb",
			"blueu",
			"purplep");'''
			cursor.execute( tobedone )
			conn.commit()
		        tobedone = """INSERT INTO cubesTBL (redr,yellowy,blackb,blueu,purplep) VALUES (24,24,24,24,24);"""
			cursor.execute( tobedone )
			conn.commit()


# This sets up the shuffled player deck (with event cards)
	def shufpd (self,nplayers):
		with sqlite3.connect('pandemic.db') as conn:
			nevents = 2* nplayers
	            	cursor = conn.cursor()
	            	tobedone = 'DROP TABLE if exists shufpd;'
	            	cursor.execute( tobedone )
			conn.commit()
			tobedone = '''CREATE TABLE shufpd(
			"name",
			"pos");'''
			cursor.execute( tobedone )
			conn.commit()
		        tobedone = """INSERT INTO shufpd (name,pos) select name,pos from edTBL limit %s;""" % (nevents) 
	  		cursor.execute( tobedone )
			conn.commit()
	        	tobedone = """INSERT INTO shufpd (name,pos) select name,ABS(RANDOM() % 500) from pdTBL;""" 
	  		cursor.execute( tobedone )
			conn.commit()

# This sets up the shuffled infection deck
	def shufid (self):
		with sqlite3.connect('pandemic.db') as conn:
	            	cursor = conn.cursor()
	            	tobedone = 'DROP TABLE if exists shufid;'
	            	cursor.execute( tobedone )
			conn.commit()
			tobedone = '''CREATE TABLE shufid(
			"name",
			"pos");'''
			cursor.execute( tobedone )
			conn.commit()
	        	tobedone = """INSERT INTO shufid (name,pos) select name,ABS(RANDOM() % 500) from idTBL;""" 
	  		cursor.execute( tobedone )
			conn.commit()



# This def draws a hand for player1
	def player1TBL (self,nplayers):
		if nplayers == 1:
			with sqlite3.connect('pandemic.db') as conn:
		            	cursor = conn.cursor()
		            	tobedone = 'DROP TABLE if exists player1TBL;'
	       		     	cursor.execute( tobedone )
				conn.commit()
				tobedone = '''CREATE TABLE player1TBL(
				"name");'''
				cursor.execute( tobedone )
				conn.commit()
		        	tobedone = 'INSERT INTO player1TBL (name) select name from shufpd ORDER BY pos DESC limit 6;'
	       		     	cursor.execute( tobedone )
		        	tobedone = 'SELECT pos FROM shufpd ORDER BY pos DESC limit 6;'
	       		     	cursor.execute( tobedone )
				conn.commit()
				answerX = cursor.fetchall ( )
				answer1 = answerX [6]
				funny1 = answer1 [0]
		        	tobedone = """DELETE FROM shufpd WHERE pos >= %s;""" % (funny1)
	       		     	cursor.execute( tobedone )
				conn.commit()

		elif nplayers == 2:
			with sqlite3.connect('pandemic.db') as conn:
		            	cursor = conn.cursor()
		            	tobedone = 'DROP TABLE if exists player1TBL;'
	       		     	cursor.execute( tobedone )
				conn.commit()
				tobedone = '''CREATE TABLE player1TBL(
				"name");'''
				cursor.execute( tobedone )
				conn.commit()
		        	tobedone = 'INSERT INTO player1TBL (name) select name from shufpd ORDER BY pos DESC limit 4;'
	       		     	cursor.execute( tobedone )
		        	tobedone = 'SELECT pos FROM shufpd ORDER BY pos DESC limit 4;'
	       		     	cursor.execute( tobedone )
				conn.commit()
				answerX = cursor.fetchall ( )
				answer1 = answerX [4]
				funny1 = answer1 [0]
		        	tobedone = """DELETE FROM shufpd WHERE pos >= %s;""" % (funny1)
	       		     	cursor.execute( tobedone )
				conn.commit()

		elif nplayers == 3:
			with sqlite3.connect('pandemic.db') as conn:
		            	cursor = conn.cursor()
		            	tobedone = 'DROP TABLE if exists player1TBL;'
	       		     	cursor.execute( tobedone )
				conn.commit()
				tobedone = '''CREATE TABLE player1TBL(
				"name");'''
				cursor.execute( tobedone )
				conn.commit()
		        	tobedone = 'INSERT INTO player1TBL (name) select name from shufpd ORDER BY pos DESC limit 3;'
	       		     	cursor.execute( tobedone )
		        	tobedone = 'SELECT pos FROM shufpd ORDER BY pos DESC limit 3;'
	       		     	cursor.execute( tobedone )
				conn.commit()
				answerX = cursor.fetchall ( )
				answer1 = answerX [3]
				funny1 = answer1 [0]
		        	tobedone = """DELETE FROM shufpd WHERE pos >= %s;""" % (funny1)
	       		     	cursor.execute( tobedone )
				conn.commit()

		elif nplayers == 4:
			with sqlite3.connect('pandemic.db') as conn:
		            	cursor = conn.cursor()
		            	tobedone = 'DROP TABLE if exists player1TBL;'
	       		     	cursor.execute( tobedone )
				conn.commit()
				tobedone = '''CREATE TABLE player1TBL(
				"name");'''
				cursor.execute( tobedone )
				conn.commit()
		        	tobedone = 'INSERT INTO player1TBL (name) select name from shufpd ORDER BY pos DESC limit 2;'
	       		     	cursor.execute( tobedone )
		        	tobedone = 'SELECT pos FROM shufpd ORDER BY pos DESC limit 2;'
	       		     	cursor.execute( tobedone )
				conn.commit()
				answerX = cursor.fetchall ( )
				answer1 = answerX [2]
				funny1 = answer1 [0]
		        	tobedone = """DELETE FROM shufpd WHERE pos >= %s;""" % (funny1)
	       		     	cursor.execute( tobedone )
				conn.commit()
		else:
			print "something went wrong"


# This def draws a hand for player4
	def player4TBL (self,nplayers):
		with sqlite3.connect('pandemic.db') as conn:
	            	cursor = conn.cursor()
	            	tobedone = 'DROP TABLE if exists player4TBL;'
       		     	cursor.execute( tobedone )
			conn.commit()
			tobedone = '''CREATE TABLE player4TBL(
			"name");'''
			cursor.execute( tobedone )
			conn.commit()
	        	tobedone = 'INSERT INTO player4TBL (name) select name from shufpd ORDER BY pos DESC limit 2;'
       		     	cursor.execute( tobedone )
	        	tobedone = 'SELECT pos FROM shufpd ORDER BY pos DESC limit 2;'
       		     	cursor.execute( tobedone )
			conn.commit()
			answerX = cursor.fetchall ( )
			answer1 = answerX [2]

			funny1 = answer1 [0]
	        	tobedone = """DELETE FROM shufpd WHERE pos >= %s;""" % (funny1)
       		     	cursor.execute( tobedone )
			conn.commit()


# This def draws a hand for player2
	def player2TBL (self,nplayers):
		if nplayers == 2:
			with sqlite3.connect('pandemic.db') as conn:
		            	cursor = conn.cursor()
		            	tobedone = 'DROP TABLE if exists player2TBL;'
	       		     	cursor.execute( tobedone )
				conn.commit()
				tobedone = '''CREATE TABLE player2TBL(
				"name");'''
				cursor.execute( tobedone )
				conn.commit()
		        	tobedone = 'INSERT INTO player2TBL (name) select name from shufpd ORDER BY pos DESC limit 4;'
	       		     	cursor.execute( tobedone )
		        	tobedone = 'SELECT pos FROM shufpd ORDER BY pos DESC limit 4;'
	       		     	cursor.execute( tobedone )
				conn.commit()
				answerX = cursor.fetchall ( )
				answer1 = answerX [4]
				funny1 = answer1 [0]
		        	tobedone = """DELETE FROM shufpd WHERE pos >= %s;""" % (funny1)

	       		     	cursor.execute( tobedone )
				conn.commit()

		elif nplayers == 3:
			with sqlite3.connect('pandemic.db') as conn:
		            	cursor = conn.cursor()
		            	tobedone = 'DROP TABLE if exists player2TBL;'
	       		     	cursor.execute( tobedone )
				conn.commit()
				tobedone = '''CREATE TABLE player2TBL(
				"name");'''
				cursor.execute( tobedone )
				conn.commit()
		        	tobedone = 'INSERT INTO player2TBL (name) select name from shufpd ORDER BY pos DESC limit 3;'
	       		     	cursor.execute( tobedone )
		        	tobedone = 'SELECT pos FROM shufpd ORDER BY pos DESC limit 3;'
	       		     	cursor.execute( tobedone )
				conn.commit()
				answerX = cursor.fetchall ( )
				answer1 = answerX [3]
				funny1 = answer1 [0]
		        	tobedone = """DELETE FROM shufpd WHERE pos >= %s;""" % (funny1)
	       		     	cursor.execute( tobedone )
				conn.commit()

		elif nplayers == 4:
			with sqlite3.connect('pandemic.db') as conn:
		            	cursor = conn.cursor()
		            	tobedone = 'DROP TABLE if exists player2TBL;'
	       		     	cursor.execute( tobedone )
				conn.commit()
				tobedone = '''CREATE TABLE player2TBL(
				"name");'''
				cursor.execute( tobedone )
				conn.commit()
		        	tobedone = 'INSERT INTO player2TBL (name) select name from shufpd ORDER BY pos DESC limit 2;'
	       		     	cursor.execute( tobedone )
		        	tobedone = 'SELECT pos FROM shufpd ORDER BY pos DESC limit 2;'
	       		     	cursor.execute( tobedone )
				conn.commit()
				answerX = cursor.fetchall ( )
				answer1 = answerX [2]
				funny1 = answer1 [0]
		        	tobedone = """DELETE FROM shufpd WHERE pos >= %s;""" % (funny1)
	       		     	cursor.execute( tobedone )
				conn.commit()
		else:
			print "error!!!"


# This def draws a hand for player3
	def player3TBL (self,nplayers):
		if nplayers == 3:
			with sqlite3.connect('pandemic.db') as conn:
		            	cursor = conn.cursor()
		            	tobedone = 'DROP TABLE if exists player3TBL;'
	       		     	cursor.execute( tobedone )
				conn.commit()
				tobedone = '''CREATE TABLE player3TBL(
				"name");'''
				cursor.execute( tobedone )
				conn.commit()
		        	tobedone = 'INSERT INTO player3TBL (name) select name from shufpd ORDER BY pos DESC limit 3;'
	       		     	cursor.execute( tobedone )
		        	tobedone = 'SELECT pos FROM shufpd ORDER BY pos DESC limit 3;'
	       		     	cursor.execute( tobedone )
				conn.commit()
				answerX = cursor.fetchall ( )
				answer1 = answerX [3]
				funny1 = answer1 [0]
		        	tobedone = """DELETE FROM shufpd WHERE pos >= %s;""" % (funny1)
	       		     	cursor.execute( tobedone )
				conn.commit()

		elif nplayers == 4:
			with sqlite3.connect('pandemic.db') as conn:
		            	cursor = conn.cursor()
		            	tobedone = 'DROP TABLE if exists player3TBL;'
	       		     	cursor.execute( tobedone )
				conn.commit()
				tobedone = '''CREATE TABLE player3TBL(
				"name");'''
				cursor.execute( tobedone )
				conn.commit()
		        	tobedone = 'INSERT INTO player3TBL (name) select name from shufpd ORDER BY pos DESC limit 2;'
	       		     	cursor.execute( tobedone )
		        	tobedone = 'SELECT pos FROM shufpd ORDER BY pos DESC limit 2;'
	       		     	cursor.execute( tobedone )
				conn.commit()
				answerX = cursor.fetchall ( )
				answer1 = answerX [2]
				funny1 = answer1 [0]
		        	tobedone = """DELETE FROM shufpd WHERE pos >= %s;""" % (funny1)
	       		     	cursor.execute( tobedone )
				conn.commit()
		else:
			print "something went wrong"


# This sets up the shuffled player deck (with event & epidemic cards, after hands drawn)
	def epTBL (self,nep):
		epidemicsaddedtopack = 0
		maxposold = 0
		with sqlite3.connect('pandemic.db') as conn:
			epidemicsaddedtopack = epidemicsaddedtopack + 1
	            	cursor = conn.cursor()
	            	tobedone = 'DROP TABLE if exists epTBL;'
	            	cursor.execute( tobedone )
			conn.commit()
			tobedone = '''CREATE TABLE epTBL(
			"name",
			"pos");'''
			cursor.execute( tobedone )
			conn.commit()
		        tobedone = """SELECT COUNT (name) FROM shufpd;""" 
	  		cursor.execute( tobedone )
			conn.commit()
			answerX = cursor.fetchone ( )
			thingy = answerX [0]
			npile = (thingy / nep)
			numberofcardsinapile = int(npile)-1
			while epidemicsaddedtopack < nep+1:
		      	 	tobedone = """SELECT pos FROM shufpd ORDER BY pos ASC;""" 
	  			cursor.execute( tobedone )
				conn.commit()
				whichcard = numberofcardsinapile * epidemicsaddedtopack
				answerZ = cursor.fetchall ()
				posnew = answerZ [whichcard]
				maxposnew = posnew [0]
				maxposuse = random.randint(maxposold, maxposnew)
		        	tobedone = '''INSERT INTO epTBL (name,pos) VALUES ('Ep%s','%s');''' % (epidemicsaddedtopack, maxposuse)
				cursor.execute( tobedone )
				conn.commit()
				epidemicsaddedtopack = epidemicsaddedtopack + 1
				maxposold = maxposnew
	            	cursor = conn.cursor()
	            	tobedone = 'INSERT INTO shufpd (name,pos) SELECT * from epTBL;'
	            	cursor.execute( tobedone )
			conn.commit()

# Sets the infection rate to 2 and the outbreak count to 0 for a game with a given number of players
	def gsTBL (self, players):
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
		       	tobedone = 'DROP TABLE if exists gsTBL;'
		       	cursor.execute( tobedone )
			conn.commit()
			tobedone = '''CREATE TABLE gsTBL(
			"ir",
			"oc",
			"players");'''
			cursor.execute( tobedone )
			conn.commit()
			tobedone = """INSERT INTO gsTBL (ir,oc,players) VALUES (2,0,%s)""" % (players)
			cursor.execute( tobedone)
			conn.commit()

	def sginfect (self):
		it = inaturn ()
		it.infectcities (9)
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = """SELECT name from BoardTBL WHERE rcube >= 1 or bcube >= 1 or ycube >= 1 or pcube >= 1 or ucube >= 1 limit 6;"""
			cursor.execute(tobedone)
			answerX = cursor.fetchall ( )
			answer4 = answerX [3]
			answer5 = answerX [4]
			answer6 = answerX [5]
			answer4r = answer4 [0]
			answer5r = answer5 [0]
			answer6r = answer6 [0]
			answer1 = answerX [0]
			answer2 = answerX [1]
			answer3 = answerX [2]
			answer1r = answer1 [0]
			answer2r = answer2 [0]
			answer3r = answer3 [0]
			tobedone = """UPDATE BoardTBL SET rcube = 2 where rcube = 1 and name is '%s' """ % (answer1r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET bcube = 2 where bcube = 1 and name is '%s' """ % (answer1r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET ycube = 2 where ycube = 1 and name is '%s' """ % (answer1r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET ucube = 2 where ucube = 1 and name is '%s' """ % (answer1r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET pcube = 2 where pcube = 1 and name is '%s' """ % (answer1r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET rcube = 2 where rcube = 1 and name is '%s' """ % (answer2r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET bcube = 2 where bcube = 1 and name is '%s' """ % (answer2r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET ycube = 2 where ycube = 1 and name is '%s' """ % (answer2r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET ucube = 2 where ucube = 1 and name is '%s' """ % (answer2r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET pcube = 2 where pcube = 1 and name is '%s' """ % (answer2r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET rcube = 2 where rcube = 1 and name is '%s' """ % (answer3r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET bcube = 2 where bcube = 1 and name is '%s' """ % (answer3r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET ycube = 2 where ycube = 1 and name is '%s' """ % (answer3r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET ucube = 2 where ucube = 1 and name is '%s' """ % (answer3r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET pcube = 2 where pcube = 1 and name is '%s' """ % (answer3r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET rcube = 3 where rcube = 1 and name is '%s' """ % (answer4r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET bcube = 3 where bcube = 1 and name is '%s' """ % (answer4r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET ycube = 3 where ycube = 1 and name is '%s' """ % (answer4r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET ucube = 3 where ucube = 1 and name is '%s' """ % (answer4r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET pcube = 3 where pcube = 1 and name is '%s' """ % (answer4r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET rcube = 3 where rcube = 1 and name is '%s' """ % (answer5r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET bcube = 3 where bcube = 1 and name is '%s' """ % (answer5r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET ycube = 3 where ycube = 1 and name is '%s' """ % (answer5r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET ucube = 3 where ucube = 1 and name is '%s' """ % (answer5r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET pcube = 3 where pcube = 1 and name is '%s' """ % (answer5r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET rcube = 3 where rcube = 1 and name is '%s' """ % (answer6r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET bcube = 3 where bcube = 1 and name is '%s' """ % (answer6r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET ycube = 3 where ycube = 1 and name is '%s' """ % (answer6r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET ucube = 3 where ucube = 1 and name is '%s' """ % (answer6r)
			cursor.execute( tobedone)
			tobedone = """UPDATE BoardTBL SET pcube = 3 where pcube = 1 and name is '%s' """ % (answer6r)
			cursor.execute( tobedone)
			conn.commit()
			
# Sets up the board for: 
# A given number of players
# on a specified boardfile such as 'board.txt'
# with a specified number of epidemics
# specified pool of event cards
# specified pool of character cards
	def startnewgame (self,players,board,epidemics,event,characters):
		sg = startinggame ()
		print "1. Laying out the board with everything."
		sg.BoardTBL (board)
		print "2. Shuffling the event cards together, so a random selection can be chosen to shuffle into the player deck."
		sg.edTBL (event) 
		print "3. Making a space for the player deck"
		sg.pdTBL ()
		sg.pddTBL ()
		print "4. Shuffling the player deck (without epidemic cards)"
		sg.shufpd (players)

		print "5. Setting out the disease cubes."
		sg.cubesTBL ()
		print "6. Drawing a hand for player One."
		sg.player1TBL (players)
		if players >= 2:
			print "7a. Also drawing a hand for player Two."
			sg.player2TBL (players)
		if players >= 3:
			print "7b. Then drawing a hand for player Three."
			sg.player3TBL (players)
		if players >= 4:
			print "7c. Finally drawing a hand for player Four."
			sg.player4TBL (players)
		else:
			print "ONE PLAYER GAME! Not sure this'll work."
		print "8. Putting starting game pieces into place"
		sg.startinglocals (players)
		sg.pdTBL ()
		sg.pddTBL ()
		print "9. Assigning player identities."
		sg.cTBL (characters)
		sg.caTBL ()
		print "10. Setting the outbreaks to Zero and the infection rate to One. Popping a research station down in Atlanta."
		sg.gsTBL (players)
		sg.startinglocals (players)
		print "11. Creating and shuffling the infection deck."
		sg.idTBL ()
		sg.iddTBL ()
		sg.shufid ()
		print "12. Infecting starting cities."
		sg.sginfect ()
		print "13. Shuffling epidemic cards into the infection deck"
		sg.epTBL (epidemics)
		print "14. LETS GO! Time to start the game!"

class inaturn:

# This def returns the location of a given player
	def getplayer (self, player):
		if player == 'player1':
			with sqlite3.connect('pandemic.db') as conn:
				cursor = conn.cursor()
				tobedone = """SELECT name FROM BoardTBL WHERE player1 = 1;"""
				cursor.execute( tobedone)
				answerA = cursor.fetchone ( )
				location = answerA [0]
			return location

		if player == 'player2':
			with sqlite3.connect('pandemic.db') as conn:
				cursor = conn.cursor()
				tobedone = """SELECT name FROM BoardTBL WHERE player2 = 1;"""
				cursor.execute( tobedone)
				answerA = cursor.fetchone ( )
				location = answerA [0]
			return location

		if player == 'player3':
			with sqlite3.connect('pandemic.db') as conn:
				cursor = conn.cursor()
				tobedone = """SELECT name FROM BoardTBL WHERE player3 = 1;"""
				cursor.execute( tobedone)
				answerA = cursor.fetchone ( )
				location = answerA [0]
			return location

		if player == 'player4':
			with sqlite3.connect('pandemic.db') as conn:
				cursor = conn.cursor()
				tobedone = """SELECT name FROM BoardTBL WHERE player4 = 1;"""
				cursor.execute( tobedone)
				answerA = cursor.fetchone ( )
				location = answerA [0]
			return location

		else:
			return 'There is no player of that name!'
				
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = """SELECT name FROM BoardTBL WHERE player1 = 1;"""
			cursor.execute( tobedone)
			answerA = cursor.fetchone ( )
			location = answerA [0]
			locinfo = """%s is located in %s""" % (player, location) 
			return locinfo



# This def returns the number of cubes in a given city
	def getcubes (self, city):
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = """SELECT * FROM BoardTBL WHERE name = '%s';""" % (city)
			cursor.execute( tobedone)
			answerA = cursor.fetchone ( )
			if answerA == None:
				return 'There is no city of that name!'
			else:			
				tobedone = """SELECT bcube FROM BoardTBL WHERE name is '%s';""" % (city)
				cursor.execute( tobedone)
				answerA= cursor.fetchone( )
				bcube= answerA [0]
				tobedone = """SELECT rcube FROM BoardTBL WHERE name is '%s';""" % (city)
				cursor.execute( tobedone)
				answerA= cursor.fetchone( )
				rcube= answerA [0]
				tobedone = """SELECT ycube FROM BoardTBL WHERE name is '%s';""" % (city)
				cursor.execute( tobedone)
				answerA= cursor.fetchone( )
				ycube= answerA [0]
				tobedone = """SELECT ucube FROM BoardTBL WHERE name is '%s';""" % (city)
				cursor.execute( tobedone)
				answerA= cursor.fetchone( )
				ucube= answerA [0]
				tobedone = """SELECT pcube FROM BoardTBL WHERE name is '%s';""" % (city)
				cursor.execute( tobedone)
				answerA= cursor.fetchone( )
				pcube= answerA [0]
				cubeinfo = """There are %s blue cubes, %s black cubes, %s red cubes, %s yellow cubes and  %s purple cubes in %s.""" % (ucube, bcube, rcube, ycube, pcube, city) 
				return cubeinfo

# This def infects cities at a given rate.
	def infectcities (self, rate):
		ci = 0
		while ci < rate:
			with sqlite3.connect('pandemic.db') as conn:
				cursor = conn.cursor()
			       	tobedone = """SELECT name,pos from shufid ORDER BY pos ASC;"""
				cursor.execute( tobedone)
				answerX = cursor.fetchone ( )
				answer1 = answerX [0] # this is the name of the card in the id
				answer2 = answerX [1] # this is the pos of the card in the id
			       	tobedone = """SELECT name,colour,ucube,bcube,rcube,ycube,pcube from BoardTBL where name is '%s';""" % (answer1)
				cursor.execute( tobedone)
				answerY = cursor.fetchone ( )
				answer3 = answerY [0] #name of place
				answer4 = answerY [1] #colour
				answer5 = answerY [2] #blue cubes
				answer6 = answerY [3] #black cubes
				answer7 = answerY [4] #red cubes
				answer8 = answerY [5] #yellow cubes
				answer9 = answerY [6] #purple cubes
				if answer4 == 'u':
					newcubes = answer5 + 1
					tobedone = """UPDATE BoardTBL SET ucube = %s WHERE name is '%s'; """ % (newcubes,answer3)	
					cursor.execute (tobedone)
					conn.commit ()
						
				elif answer4 == 'b':
					newcubes = answer6 + 1
					tobedone = """UPDATE BoardTBL SET bcube = %s WHERE name is '%s'; """ % (newcubes,answer3)	
					cursor.execute (tobedone)
					conn.commit ()
						
				elif answer4 == 'r':
					newcubes = answer7 + 1
					tobedone = """UPDATE BoardTBL SET rcube = %s WHERE name is '%s'; """ % (newcubes,answer3)	
					cursor.execute (tobedone)
					conn.commit ()
						
				elif answer4 == 'y':
					newcubes = answer8 + 1
					tobedone = """UPDATE BoardTBL SET ycube = %s WHERE name is '%s'; """ % (newcubes,answer3)	
					cursor.execute (tobedone)
					conn.commit ()
						
				elif answer4 == 'p':
					newcubes = answer9 + 1
					tobedone = """UPDATE BoardTBL SET pcube = %s WHERE name is '%s'; """ % (newcubes,answer3)	
					cursor.execute (tobedone)
					conn.commit ()
						
				else:
					print "something has gone wrong"

				ci = ci + 1
		        	tobedone = """DELETE FROM shufid WHERE name is '%s';""" % (answer3)
	       		     	cursor.execute( tobedone )
				tobedone = """INSERT INTO iddTBL (name) VALUES ('%s')""" % (answer3)
	       		     	cursor.execute( tobedone )
				conn.commit()

# This moves a player from one location to another
	def move (self, player, location, destination):
		with sqlite3.connect('pandemic.db') as conn:
		       	cursor = conn.cursor()
	            	tobedone = """UPDATE BoardTBL set %s = 0 WHERE name is '%s';""" % (player, location)
	            	cursor.execute( tobedone )
	            	tobedone = """UPDATE BoardTBL set %s = 1 WHERE name is '%s';""" % (player, destination)
	            	cursor.execute( tobedone )
			conn.commit()

# This returns the name of cities with a given number of cubes
	def getxcube (self,cube,numb):
		with sqlite3.connect('pandemic.db') as conn:
		       	cursor = conn.cursor()
	            	tobedone = """SELECT count (name) FROM BoardTBL WHERE %s = %s;""" % (cube,numb)
			print tobedone
	            	cursor.execute( tobedone )
			numbans= cursor.fetchone( )
	            	tobedone = """SELECT name FROM BoardTBL WHERE %s = %s;""" % (cube,numb)	
			print tobedone
	            	cursor.execute( tobedone )
			naans= cursor.fetchall ( )
			answer = numbans, naans
			print answer
			return answer

