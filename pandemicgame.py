#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:
import sys
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
			"colour",
			"pos" INTEGER);'''
			cursor.execute( tobedone )
			conn.commit()
		        tobedone = """INSERT INTO pdTBL (name,colour) select name,colour from BoardTBL;""" 
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
			"name",
			"colour");'''
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
			"pos" INTEGER);'''
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
			conn.commit()

# This sets up the event deck and populates it
	def edTBL (self,event):
		with sqlite3.connect('pandemic.db') as conn:
	            	cursor = conn.cursor()
	            	tobedone = 'DROP TABLE if exists edTBL;'
	            	cursor.execute( tobedone )
			conn.commit()
			tobedone = '''CREATE TABLE edTBL(
			"name",
			"pos" INTEGER);'''
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
			"pos" INTEGER,
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
			"rcube",
			"ycube",
			"bcube",
			"ucube",
			"pcube");'''
			cursor.execute( tobedone )
			conn.commit()
		        tobedone = """INSERT INTO cubesTBL (rcube,ycube,bcube,ucube,pcube) VALUES (24,24,24,24,12);"""
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
			"colour",
			"pos" INTEGER INTEGER);'''
			cursor.execute( tobedone )
			conn.commit()
		        tobedone = """INSERT INTO shufpd (name,pos) select name,pos from edTBL limit %s;""" % (nevents) 
	  		cursor.execute( tobedone )
			conn.commit()
	        	tobedone = """INSERT INTO shufpd (name,colour,pos) select name,colour,ABS(RANDOM() % 500) from pdTBL;""" 
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
			"pos" INTEGER);'''
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
				"name","colour");'''
				cursor.execute( tobedone )
				conn.commit()
		        	tobedone = 'INSERT INTO player1TBL (name,colour) select name,colour from shufpd ORDER BY pos DESC limit 6;'
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
				"name","colour");'''
				cursor.execute( tobedone )
				conn.commit()
		        	tobedone = 'INSERT INTO player1TBL (name,colour) select name,colour from shufpd ORDER BY pos DESC limit 4;'
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
				"name","colour");'''
				cursor.execute( tobedone )
				conn.commit()
		        	tobedone = 'INSERT INTO player1TBL (name,colour) select name,colour from shufpd ORDER BY pos DESC limit 3;'
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
				"name","colour");'''
				cursor.execute( tobedone )
				conn.commit()
		        	tobedone = 'INSERT INTO player1TBL (name,colour) select name,colour from shufpd ORDER BY pos DESC limit 2;'
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
			"name","colour");'''
			cursor.execute( tobedone )
			conn.commit()
	        	tobedone = 'INSERT INTO player4TBL (name,colour) select name,colour from shufpd ORDER BY pos DESC limit 2;'
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
				"name","colour");'''
				cursor.execute( tobedone )
				conn.commit()
		        	tobedone = 'INSERT INTO player2TBL (name,colour) select name,colour from shufpd ORDER BY pos DESC limit 4;'
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
				"name","colour");'''
				cursor.execute( tobedone )
				conn.commit()
		        	tobedone = 'INSERT INTO player2TBL (name,colour) select name,colour from shufpd ORDER BY pos DESC limit 3;'
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
				"name","colour");'''
				cursor.execute( tobedone )
				conn.commit()
		        	tobedone = 'INSERT INTO player2TBL (name,colour) select name,colour from shufpd ORDER BY pos DESC limit 2;'
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
				"name","colour");'''
				cursor.execute( tobedone )
				conn.commit()
		        	tobedone = 'INSERT INTO player3TBL (name,colour) select name,colour from shufpd ORDER BY pos DESC limit 3;'
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
				"name","colour");'''
				cursor.execute( tobedone )
				conn.commit()
		        	tobedone = 'INSERT INTO player3TBL (name,colour) select name,colour from shufpd ORDER BY pos DESC limit 2;'
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
			"pos" INTEGER);'''
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
			"players",
			"ec",
			"ap",
			"action");'''
			cursor.execute( tobedone )
			conn.commit()
			tobedone = """INSERT INTO gsTBL (ir,oc,players,ec,ap,action) VALUES (2,0,%s,0,'player1',4)""" % (players)
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

			count2cu = 0
			count2cr = 0
			count2cy = 0
			count2cb = 0
			count2cp = 0

			thing = it.getxcube ('ucube', '2')
			blank = thing [1]
			if blank != []:
				supercount = thing [0]
				count2cu = supercount [0]

			thing = it.getxcube ('rcube', '2')
			blank = thing [1]
			if blank != []:
				supercount = thing [0]
				count2cr = supercount [0]

			thing = it.getxcube ('ycube', '2')
			blank = thing [1]
			if blank != []:
				supercount = thing [0]
				count2cy = supercount [0]

			thing = it.getxcube ('bcube', '2')
			blank = thing [1]
			if blank != []:
				supercount = thing [0]
				count2cb = supercount [0]

			ucount = 0
			bcount = 0
			ycount = 0
			pcount = 0
			rcount = 0
			while ucount < count2cu:
				it.usecube ('ucube')
				ucount = ucount +1
			while rcount < count2cr:
				it.usecube ('rcube')
				rcount = rcount +1
			while ycount < count2cy:
				it.usecube ('ycube')
				ycount = ycount +1
			while bcount < count2cb:
				it.usecube ('bcube')
				bcount = bcount +1
			while pcount < count2cp:
				it.usecube ('pcube')
				pcount = pcount +1
			

			count3cu = 0
			count3cr = 0
			count3cy = 0
			count3cb = 0
			count3cp = 0

			thing = it.getxcube ('ucube', '3')
			blank = thing [1]
			if blank != []:
				supercount = thing [0]
				count3cu = supercount [0]

			thing = it.getxcube ('rcube', '3')
			blank = thing [1]
			if blank != []:
				supercount = thing [0]
				count3cr = supercount [0]

			thing = it.getxcube ('ycube', '3')
			blank = thing [1]
			if blank != []:
				supercount = thing [0]
				count3cy = supercount [0]

			thing = it.getxcube ('bcube', '3')
			blank = thing [1]
			if blank != []:
				supercount = thing [0]
				count3cb = supercount [0]

			ucount = 0
			bcount = 0
			ycount = 0
			pcount = 0
			rcount = 0
			while ucount < count3cu:
				it.usecube ('ucube')
				it.usecube ('ucube')
				ucount = ucount +1
			while rcount < count3cr:
				it.usecube ('rcube')
				it.usecube ('rcube')
				rcount = rcount +1
			while ycount < count3cy:
				it.usecube ('ycube')
				it.usecube ('ycube')
				ycount = ycount +1
			while bcount < count3cb:
				it.usecube ('bcube')
				it.usecube ('bcube')
				bcount = bcount +1
			while pcount < count3cp:
				it.usecube ('pcube')
				it.usecube ('pcube')
				pcount = pcount +1


# Sets up the board for: 
# A given number of players
# on a specified boardfile such as 'board.txt'
# with a specified number of epidemics
# specified pool of event cards
# specified pool of character cards
	def startnewgame (self,players,board,epidemics,event,characters):
		sg = startinggame ()
		g = game ()
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
		elif players >= 3:
			print "7b. Then drawing a hand for player Three."
			sg.player3TBL (players)
		elif players >= 4:
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
		g.start ()


# Stats a new game as above, but without the printing
	def startnewgameq (self,players,board,epidemics,event,characters):
		sg = startinggame ()
		sg.BoardTBL (board)
		sg.edTBL (event) 
		sg.pdTBL ()
		sg.pddTBL ()
		sg.shufpd (players)
		sg.cubesTBL ()
		sg.player1TBL (players)
		if players >= 2:
			sg.player2TBL (players)
		if players >= 3:
			sg.player3TBL (players)
		if players >= 4:
			sg.player4TBL (players)
		sg.startinglocals (players)
		sg.pdTBL ()
		sg.pddTBL ()
		sg.cTBL (characters)
		sg.caTBL ()
		sg.gsTBL (players)
		sg.startinglocals (players)
		sg.idTBL ()
		sg.iddTBL ()
		sg.shufid ()
		sg.sginfect ()
		sg.epTBL (epidemics)

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



# This def returns the number of cubes of all colours in a given city
	def getcityallcubes (self,city):
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
		it = inaturn ()
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
					if newcubes < 4:
						it.usecube ('ucube')
						
				elif answer4 == 'b':
					newcubes = answer6 + 1
					tobedone = """UPDATE BoardTBL SET bcube = %s WHERE name is '%s'; """ % (newcubes,answer3)	
					cursor.execute (tobedone)
					conn.commit ()
					if newcubes < 4:
						it.usecube ('bcube')
						
				elif answer4 == 'r':
					newcubes = answer7 + 1
					tobedone = """UPDATE BoardTBL SET rcube = %s WHERE name is '%s'; """ % (newcubes,answer3)	
					cursor.execute (tobedone)
					conn.commit ()
					if newcubes < 4:
						it.usecube ('rcube')
						
				elif answer4 == 'y':
					newcubes = answer8 + 1
					tobedone = """UPDATE BoardTBL SET ycube = %s WHERE name is '%s'; """ % (newcubes,answer3)	
					cursor.execute (tobedone)
					conn.commit ()
					if newcubes < 4:
						it.usecube ('ycube')
						
				elif answer4 == 'p':
					newcubes = answer9 + 1
					tobedone = """UPDATE BoardTBL SET pcube = %s WHERE name is '%s'; """ % (newcubes,answer3)	
					cursor.execute (tobedone)
					conn.commit ()
					if newcubes < 4:
						it.usecube ('pcube')
						
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
	            	cursor.execute( tobedone )
			numbans= cursor.fetchone( )
	            	tobedone = """SELECT name FROM BoardTBL WHERE %s = %s;""" % (cube,numb)	
	            	cursor.execute( tobedone )
			naans= cursor.fetchall ( )
			answer = numbans, naans
			return answer

# Thiis returns the outbreak count
	def getoc (self):
		with sqlite3.connect('pandemic.db') as conn:
		       	cursor = conn.cursor()
	            	tobedone = """SELECT oc FROM gsTBL;""" 
	            	cursor.execute( tobedone )
			found = cursor.fetchone( )
			oc = found [0]
			return oc

# Thiis returns the infection rate
	def getir (self):
		with sqlite3.connect('pandemic.db') as conn:
		       	cursor = conn.cursor()
	            	tobedone = """SELECT ir FROM gsTBL;""" 
	            	cursor.execute( tobedone )
			found = cursor.fetchone( )
			ir = found [0]
			return ir

	def gethand (self, player):
		with sqlite3.connect('pandemic.db') as conn:
		       	cursor = conn.cursor()
	            	tobedone = """SELECT name FROM %sTBL;""" % (player)
	            	cursor.execute( tobedone )
			found = cursor.fetchall( )
			return found

 
# This def returns the number of cubes of a given colour in a given city
	def getcitycubes (self,cube,city):
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = """SELECT * FROM BoardTBL WHERE name = '%s';""" % (city)
			cursor.execute( tobedone)
			answerA = cursor.fetchone ( )
			if answerA == None:
				return 'There is no city of that name!'
			else:			
				tobedone = """SELECT %s FROM BoardTBL WHERE name is '%s';""" % (cube, city)
				cursor.execute( tobedone)
				answerA= cursor.fetchone( )
				cubes = answerA [0]
				return cubes

# This def returns the total remaining cubes of a given colour
	def getcubes (self,cube):
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = """SELECT %s FROM cubesTBL;""" % (cube)
			cursor.execute( tobedone)
			cubes = cursor.fetchone ( )
			cubeleft = cubes [0]
			return cubeleft
		
# This def reduces the total remaining cubes of a given colour by 1
	def usecube (self,cube):
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = """SELECT %s FROM cubesTBL;""" % (cube)
			cursor.execute( tobedone)
			cubes = cursor.fetchone ( )
			cubeleft = cubes [0]
			conn.commit ()
			newcube = cubeleft - 1
			tobedone = """UPDATE cubesTBL SET %s = %s;""" % (cube, newcube)
			cursor.execute( tobedone)
			conn.commit ()

# This def checks the infectiondeck discard pile
	def getidd (self):
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = """SELECT name FROM iddTBL;"""
			cursor.execute( tobedone)
			iddcont = cursor.fetchall ( )
			conn.commit ()
			return iddcont

# This def checks the player deck discard pile
	def getpdd (self):
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = """SELECT name FROM pddTBL;"""
			cursor.execute( tobedone)
			pddcont = cursor.fetchall ( )
			conn.commit ()
			return pddcont

	def pdraw (self, player):
		it = inaturn ()
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = """SELECT name from shufpd ORDER BY pos ASC limit 1;"""
       		     	cursor.execute( tobedone )
			answerX = cursor.fetchall ( )
			answer1 = answerX [0]
			maybeep = answer1 [0]

			if maybeep == 'Ep1':
				print "drawn an epidemic!"
				it.epidemic ()
			elif maybeep == 'Ep2':
				print "drawn an epidemic!"
				it.epidemic ()
			elif maybeep == 'Ep3':
				print "drawn an epidemic!"
				it.epidemic ()
			elif maybeep == 'Ep4':
				print "drawn an epidemic!"
				it.epidemic ()
			elif maybeep == 'Ep5':
				print "drawn an epidemic!"
				it.epidemic ()
			elif maybeep == 'Ep6':
				print "drawn an epidemic!"
				it.epidemic ()
			elif maybeep == 'Ep7':
				print "drawn an epidemic!"
				it.epidemic ()
			elif maybeep == 'Ep8':
				print "drawn an epidemic!"
				it.epidemic ()
			elif maybeep == 'Ep9':
				print "drawn an epidemic!"
				it.epidemic ()
			else:
				tobedone = 'INSERT INTO %sTBL (name) select name from shufpd ORDER BY pos ASC limit 1;' % (player)
	       		     	cursor.execute( tobedone )
		        	tobedone = 'SELECT pos FROM shufpd ORDER BY pos ASC limit 1;'
       			     	cursor.execute( tobedone )
				conn.commit()
				answerX = cursor.fetchall ( )
				answer1 = answerX [0]
				funny1 = answer1 [0]
	        		tobedone = """DELETE FROM shufpd WHERE pos <= %s;""" % (funny1)
       		     		cursor.execute( tobedone )
				conn.commit()

	def discard (self, player, card):
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
	        	tobedone = """DELETE FROM %sTBL WHERE name is '%s';""" % (player, card)
			cursor.execute( tobedone )
	        	tobedone = """INSERT INTO pddTBL (name) VALUES ('%s');""" % (card)
			cursor.execute( tobedone )
			conn.commit()

	def epidemic ( self):
		with sqlite3.connect('pandemic.db') as conn:
			it = inaturn ()
			cursor = conn.cursor()
			# increasing the infection rate
	        	tobedone = """SELECT ec FROM gsTBL;"""
			cursor.execute( tobedone )
			answerX = cursor.fetchone ( )
			ec = answerX [0]
			ec = ec + 1
			if ec == 3:
	        		tobedone = """UPDATE gsTBL SET ir = 3;"""
				cursor.execute( tobedone )
			if ec == 4:
	        		tobedone = """UPDATE gsTBL SET ir = 3;"""
				cursor.execute( tobedone )
			if ec >= 5:
	        		tobedone = """UPDATE gsTBL SET ir = 4;"""
				cursor.execute( tobedone )
	        	tobedone = """UPDATE gsTBL SET ec = %s;""" % (ec)
			cursor.execute( tobedone )
			conn.commit()
			
			# infecting bottom card of infection deck
			tobedone = """SELECT name,pos from shufid ORDER BY pos DESC;"""
			cursor.execute( tobedone)
			answerX = cursor.fetchone ( )
			answer1 = answerX [0] # this is the name of the card in the id
			answer2 = answerX [1] # this is the pos of the card in the id
		       	tobedone = """SELECT name,colour FROM BoardTBL where name is '%s';""" % (answer1)
			cursor.execute( tobedone
)
			answerY = cursor.fetchone ( )
			answer3 = answerY [0] #name of place
			answer4 = answerY [1] #colour
			print "%s is now infected!" % (answer3)
			it.ic (answer4,answer3)
			it.ic (answer4,answer3)
			it.ic (answer4,answer3)
		        tobedone = """DELETE FROM shufid WHERE name is '%s';""" % (answer3)
	       		cursor.execute( tobedone )
			tobedone = """INSERT INTO iddTBL (name) VALUES ('%s')""" % (answer3)
	       		cursor.execute( tobedone )
			conn.commit()
				
			conn.commit()
			# shuffling the idd to the top of the infection deck	
	        	tobedone = """UPDATE shufid SET pos = ABS(RANDOM() % 500)+500;""" 
	  		cursor.execute( tobedone )
	        	tobedone = """INSERT INTO shufid (name,pos) select name,ABS(RANDOM() % 500) from iddTBL;""" 
	  		cursor.execute( tobedone )
			conn.commit()

	def co (self):
		it = inaturn ()
                listofcol = ['ucube','ycube','rcube','bcube','pcube']
                listofnumb = [7,6,5,4]
                listofnumb2 = [9,10,11,12]
                for a in listofcol:
                        for b in listofnumb:
                                city = it.getxcube (a,b)
				if city [0][0] >= 1:
					d = 0
					while city [0][0] > d:
						outbreakc = city [1][d][0]
						print "There has been an outbreak in %s!" % (outbreakc)
						with sqlite3.connect('pandemic.db') as conn:
							cursor = conn.cursor()
							oldoc = it.getoc ()
							newoc = oldoc +1
						       	tobedone = """UPDATE gsTBL SET oc = %s;""" % (newoc)
							cursor.execute( tobedone )
							conn.commit ()
						       	tobedone = """UPDATE BoardTBL SET %s = 9 WHERE name is '%s';""" % (a,outbreakc)
							cursor.execute( tobedone )
							conn.commit ()
					        	tobedone = """SELECT connect FROM BoardTBL WHERE name is '%s';""" % (outbreakc)
							cursor.execute( tobedone )
							answerX = cursor.fetchone ( )
							connect = int (answerX [0])
							t = 0
							timestodo = connect - 1
							while t <= timestodo:
								t = t + 1
								use = str (t)
								find = "co"+use
					        		tobedone = """SELECT %s, colour FROM BoardTBL WHERE name is '%s';""" % (find,outbreakc)
								cursor.execute( tobedone )
								answerX = cursor.fetchone ( )
								connect = answerX [0]
								colour = answerX [1]
								print "The infection has spread from %s to %s." % (outbreakc, connect)
								it.ic (colour,connect)
								
							
						d = d + 1
                for a in listofcol:
                        for b in listofnumb:
                                city = it.getxcube (a,b)
				if city [0][0] >= 1:
					d = 0
					while city [0][0] > d:
						outbreakc = city [1][d][0]
						print "There has been an outbreak in %s!" % (outbreakc)
						with sqlite3.connect('pandemic.db') as conn:
							cursor = conn.cursor()
						       	tobedone = """UPDATE BoardTBL SET %s = 9 WHERE name is '%s';""" % (a,outbreakc)
							cursor.execute( tobedone )
							conn.commit ()
					        	tobedone = """SELECT connect FROM BoardTBL WHERE name is '%s';""" % (outbreakc)
							cursor.execute( tobedone )
							answerX = cursor.fetchone ( )
							connect = int (answerX [0])
							t = 0
							timestodo = connect - 1
							while t <= timestodo:
								t = t + 1
								use = str (t)
								find = "co"+use
					        		tobedone = """SELECT %s, colour FROM BoardTBL WHERE name is '%s';""" % (find,outbreakc)
								cursor.execute( tobedone )
								answerX = cursor.fetchone ( )
								connect = answerX [0]
								colour = answerX [1]
								print "The infection has spread from %s to %s." % (outbreakc, connect)
								it.ic (colour,connect)
								
							
						d = d + 1
                for a in listofcol:
                        for b in listofnumb:
                                city = it.getxcube (a,b)
				if city [0][0] >= 1:
					d = 0
					while city [0][0] > d:
						outbreakc = city [1][d][0]
						print "There has been an outbreak in %s!" % (outbreakc)
						with sqlite3.connect('pandemic.db') as conn:
							cursor = conn.cursor()
						       	tobedone = """UPDATE BoardTBL SET %s = 9 WHERE name is '%s';""" % (a,outbreakc)
							cursor.execute( tobedone )
							conn.commit ()
					        	tobedone = """SELECT connect FROM BoardTBL WHERE name is '%s';""" % (outbreakc)
							cursor.execute( tobedone )
							answerX = cursor.fetchone ( )
							connect = int (answerX [0])
							t = 0
							timestodo = connect - 1
							while t <= timestodo:
								t = t + 1
								use = str (t)
								find = "co"+use
					        		tobedone = """SELECT %s, colour FROM BoardTBL WHERE name is '%s';""" % (find,outbreakc)
								cursor.execute( tobedone )
								answerX = cursor.fetchone ( )
								connect = answerX [0]
								colour = answerX [1]
								print "The infection has spread from %s to %s." % (outbreakc, connect)
								it.ic (colour,connect)
								
							
						d = d + 1
                for a in listofcol:
                        for b in listofnumb:
                                city = it.getxcube (a,b)
				if city [0][0] >= 1:
					d = 0
					while city [0][0] > d:
						outbreakc = city [1][d][0]
						print "There has been an outbreak in %s!" % (outbreakc)
						with sqlite3.connect('pandemic.db') as conn:
							cursor = conn.cursor()
						       	tobedone = """UPDATE BoardTBL SET %s = 9 WHERE name is '%s';""" % (a,outbreakc)
							cursor.execute( tobedone )
							conn.commit ()
					        	tobedone = """SELECT connect FROM BoardTBL WHERE name is '%s';""" % (outbreakc)
							cursor.execute( tobedone )
							answerX = cursor.fetchone ( )
							connect = int (answerX [0])
							t = 0
							timestodo = connect - 1
							while t <= timestodo:
								t = t + 1
								use = str (t)
								find = "co"+use
					        		tobedone = """SELECT %s, colour FROM BoardTBL WHERE name is '%s';""" % (find,outbreakc)
								cursor.execute( tobedone )
								answerX = cursor.fetchone ( )
								connect = answerX [0]
								colour = answerX [1]
								print "The infection has spread from %s to %s." % (outbreakc, connect)
								it.ic (colour,connect)
								
							
						d = d + 1
                for a in listofcol:
                        for b in listofnumb2:
                                city = it.getxcube (a,b)
				if city [0][0] >= 1:
					d = 0
					while city [0][0] > d:
						outbreakc = city [1][d][0]
						with sqlite3.connect('pandemic.db') as conn:
							cursor = conn.cursor()
							outbreakc = city [1][d][0]
						       	tobedone = """UPDATE BoardTBL SET %s = 3 WHERE name is '%s';""" % (a,outbreakc)
							cursor.execute( tobedone )
							conn.commit ()
						d = d + 1
					 
		

	def ic (self, colour, city):
		it = inaturn ()
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			cube = colour+'cube'
			tobedone = """SELECT %s from BoardTBL where name is '%s';""" % (cube,city)
			cursor.execute( tobedone)
			found = cursor.fetchone ( )
			newcubes = found [0] + 1
			tobedone = """UPDATE BoardTBL SET %s = %s WHERE name is '%s'; """ % (cube,newcubes,city)	
			cursor.execute (tobedone)
			conn.commit ()
			if newcubes <= 3:
				it.usecube (cube)


	def action (self):
		g = game ()
		it = inaturn ()
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = """SELECT action from gsTBL;""" 
			cursor.execute( tobedone)
			found = cursor.fetchone ( )
			newaction = found [0] - 1
			tobedone = """UPDATE gsTBL SET action = %s; """ % (newaction)	
			cursor.execute (tobedone)
			conn.commit ()
			if newaction == 0:
				tobedone = """SELECT ap FROM gsTBL;"""
				cursor.execute (tobedone)
				found  = cursor.fetchone ( )
				player = found [0]
				print "End of %s's turn. Drawing cards." % (player)
				it.pdraw (player)
				it.pdraw (player)
				ir = it.getir ()
				print "Infecting %s cities." % (ir)
				it.infectcities	(ir)
				print "checking for outbreaks!"
				it.co ()
				oc = it.getoc ()
				if oc >= 8:
					print "You've lost the game"
					g.gameover ()
				else:
					print "%s outbreaks so far, 8 or more and you loose the game" % (oc)
				tobedone = """SELECT players FROM gsTBL;"""
				cursor.execute (tobedone)
				found  = cursor.fetchone ( )
				noplayer = found [0]
				if noplayer == 1:
					print "One player game, returning priority to player 1"
				if noplayer == 2:
					print "Moving priority to next player"
					if player == 'player1':
						tobedone = """UPDATE gsTBL SET ap = 'player2'; """
						cursor.execute (tobedone)
						conn.commit ()
					if player == 'player2':
						tobedone = """UPDATE gsTBL SET ap = 'player1'; """
						cursor.execute (tobedone)
						conn.commit ()
				if noplayer == 3:
					print "Moving priority to next player"
					if player == 'player1':
						tobedone = """UPDATE gsTBL SET ap = 'player2'; """
						cursor.execute (tobedone)
						conn.commit ()
					if player == 'player2':
						tobedone = """UPDATE gsTBL SET ap = 'player3'; """
						cursor.execute (tobedone)
						conn.commit ()
					if player == 'player3':
						tobedone = """UPDATE gsTBL SET ap = 'player1'; """
						cursor.execute (tobedone)
						conn.commit ()
				if noplayer == 4:
					print "Moving priority to next player"
					if player == 'player1':
						tobedone = """UPDATE gsTBL SET ap = 'player2'; """
						cursor.execute (tobedone)
						conn.commit ()
					if player == 'player2':
						tobedone = """UPDATE gsTBL SET ap = 'player3'; """
						cursor.execute (tobedone)
						conn.commit ()
					if player == 'player3':
						tobedone = """UPDATE gsTBL SET ap = 'player4'; """
						cursor.execute (tobedone)
						conn.commit ()
					if player == 'player4':
						tobedone = """UPDATE gsTBL SET ap = 'player1'; """
						cursor.execute (tobedone)
						conn.commit ()
				tobedone = """UPDATE gsTBL set action = 4;"""
				cursor.execute (tobedone)
				conn.commit ()
				

	def rc (self,colour,city):
		with sqlite3.connect('pandemic.db') as conn:
		       	cursor = conn.cursor()
	            	tobedone = """SELECT %s FROM BoardTBL WHERE name is '%s';""" % (colour,city)
	            	cursor.execute( tobedone )
			found  = cursor.fetchone ( )
			cubes = found [0]
			if cubes == 0:
				print "No cubes of that colour found!"
			else:
				cubes = cubes - 1
				tobedone = """UPDATE BoardTBL SET %s = %s WHERE name is '%s';""" % (colour,cubes,city)
		            	cursor.execute( tobedone )
				tobedone = """SELECT %s FROM cubesTBL;""" % (colour)
	            		cursor.execute( tobedone )
				found  = cursor.fetchone ( )
				cubepool = found [0]
				cubepool = cubepool + 1
				tobedone = """UPDATE cubesTBL SET %s = %s;""" % (colour,cubepool)
		            	cursor.execute( tobedone )
				conn.commit ()
		
				
	def getap (self):
		it = inaturn ()
		with sqlite3.connect('pandemic.db') as conn:
		   	cursor = conn.cursor()
			tobedone = """SELECT ap FROM gsTBL;"""
			cursor.execute (tobedone)
			answerX = cursor.fetchone ()
			ap = answerX [0]
			return ap 
					
						
		

class playeraction:
        def direct (self,player,card):
		it = inaturn ()
		it.discard (player,card)
		location = it.getplayer (player)
		it.move (player,location,card)
		print "%s has taken a direct flight to %s" % (player, card)
		it.action ()
	
	def trainboat (self,player,location,destination):
		it = inaturn ()
		location = it.getplayer (player)	
		it.move (player,location,destination)
		print "%s has moved from %s to %s" % (player, location, destination)
		it.action ()

	def charter (self,player,card,destination):
		it = inaturn ()
		location = it.getplayer (player)
		if location != card:
			print "You need to play the card that matches your location."
		if location == card:
			it.discard (player,card)
			it.move (player,location,destination)
			print "%s has taken a charter flight from %s to %s" % (player, card, destination)
			it.action ()
			
		else:
			print "ERROR!"
	

	def shuttle (self,player,destination):
		it = inaturn ()
		location = it.getplayer (player)
		with sqlite3.connect('pandemic.db') as conn:
		       	cursor = conn.cursor()
	            	tobedone = "SELECT rstation FROM BoardTBL WHERE name is '%s';" % (location)
	            	cursor.execute( tobedone )
			found  = cursor.fetchone ( )
			norstation1 = found [0]
	            	tobedone = """SELECT rstation FROM BoardTBL WHERE name is '%s';""" % (destination)
	            	cursor.execute( tobedone )
			found  = cursor.fetchone ( )
			norstation2 = found [0]
		if norstation1 != 1:
			print "No research station in %s, can't take a shuttle flight from here" % (location)
		if norstation2 != 1:
			print "No research station in %s, can't take a shuttle flight from here" % (destination)
		else:
			it.move (player,location,destination)
			it.action ()


	def treat (self,player,cube):
		it = inaturn ()
		location = it.getplayer (player)
		it.rc (cube,location)
		it.action ()
		
class game:

        def start (self):
		g = game ()
                print """What would you like to do? 
1- Find out about the board state.
2- Take an action.
3- Quit."""
                thing = raw_input ('>')
                if thing == '1':
                        g.info ()
		elif thing == '2':
			g.action ()
		elif thing == '3':
			print "Are you sure? If so press Q."
			thing = raw_input ('>')
			if thing == 'q':
				print "goodbye!"
			elif thing == 'Q':
				print "goodbye!"
			else:
				g.start ()
		else:
			print "Type either 1, 2 or 3."
			g.start ()



        def info (self):
		g = game ()
                print """What do you want to know?
1. About a city?
2. How many cities with 3 cubes of a given or any colour in?
3. How many cities with 2 cubes of a given or any colour in?
4. How many cities with 1 cube of a given or any colour in?
5. Where am I?
6. What is in my hand?"""
                thing = raw_input ('>')
                if thing == '1':
			g.cityinfo ()
		elif thing == '2':	
			g.cube3info ()
		elif thing == '3':	
			g.cube2info ()
		elif thing == '4':	
			g.cube1info ()
		elif thing == '5':	
			g.playerlocinfo ()
		elif thing == '6':	
			g.handinfo ()
		else:
			print "Type either 1,2,3,4,5 or 6"
			g.action

	def cityinfo (self):
		it = inaturn ()
		g = game ()
		print "What city?"
		answer = raw_input ('>')
		findout = it.getcityallcubes (answer)
		if findout == 'There is no city of that name!':
			print findout
			with sqlite3.connect('pandemic.db') as conn:
		       		cursor = conn.cursor()
				tobedone = """SELECT name FROM BoardTBL;"""
				cursor.execute (tobedone)
				answerX = cursor.fetchall ()
				print "The cities are listed below."
				for a in answerX:
					print a [0]
				g.cityinfo ()
		else:
			print findout
			g.start ()
			

	def cube3info (self):
		it = inaturn ()
		g = game ()
		print """What colour?
1. Blue
2. Yellow
3. Red
4. Black
5. All"""
		answer = raw_input ('>')
		if answer == '1':
			findout = it.getxcube ('ucube',3)
			print "There are %s cities with 3 blue cubes, in:" % (findout [0][0])
			listc = findout [1]
			for a in listc:
				print a [0]
			g.start () 
		elif answer == '2':
			findout = it.getxcube ('ycube',3)
			print "There are %s cities with 3 yellow cubes, in:" % (findout [0][0])
			listc = findout [1]
			for a in listc:
				print a [0]
			g.start () 
		elif answer == '3':
			findout = it.getxcube ('rcube',3)
			print "There are %s cities with 3 red cubes, in:" % (findout [0][0])
			listc = findout [1]
			for a in listc:
				print a [0]
			g.start () 
		elif answer == '4':
			findout = it.getxcube ('bcube',3)
			print "There are %s cities with 3 black cubes, in:" % (findout [0][0])
			listc = findout [1]
			for a in listc:
				print a [0]
			g.start () 
		elif answer == '5':
			findout1 = it.getxcube ('bcube',3)
			findout2 = it.getxcube ('ucube',3)
			findout3 = it.getxcube ('ycube',3)
			findout4 = it.getxcube ('rcube',3)
			totalfound =findout1 [0][0] + findout2 [0][0] + findout3 [0][0] + findout4 [0][0] 
			print "There are %s cities with 3 cubes, in:" % (totalfound)
			listc = findout1 [1]
			for a in listc:
				print a [0]
			listc = findout2 [1]
			for a in listc:
				print a [0]
			listc = findout3 [1]
			for a in listc:
				print a [0]
			listc = findout4 [1]
			for a in listc:
				print a [0]
			g.start () 
		else:
			print "Please answer 1,2,3 or 4."
			g.cube3info ()

	def cube2info (self):
		it = inaturn ()
		g = game ()
		print """What colour?
1. Blue
2. Yellow
3. Red
4. Black
5. All"""
		answer = raw_input ('>')
		if answer == '1':
			findout = it.getxcube ('ucube',2)
			print "There are %s cities with 2 blue cubes, in:" % (findout [0][0])
			listc = findout [1]
			for a in listc:
				print a [0]
			g.start () 
		elif answer == '2':
			findout = it.getxcube ('ycube',2)
			print "There are %s cities with 2 yellow cubes, in:" % (findout [0][0])
			listc = findout [1]
			for a in listc:
				print a [0]
			g.start () 
		elif answer == '3':
			findout = it.getxcube ('rcube',2)
			print "There are %s cities with 2 red cubes, in:" % (findout [0][0])
			listc = findout [1]
			for a in listc:
				print a [0]
			g.start () 
		elif answer == '4':
			findout = it.getxcube ('bcube',2)
			print "There are %s cities with 2 black cubes, in:" % (findout [0][0])
			listc = findout [1]
			for a in listc:
				print a [0]
			g.start () 
		elif answer == '5':
			findout1 = it.getxcube ('bcube',2)
			findout2 = it.getxcube ('ucube',2)
			findout3 = it.getxcube ('ycube',2)
			findout4 = it.getxcube ('rcube',2)
			totalfound =findout1 [0][0] + findout2 [0][0] + findout3 [0][0] + findout4 [0][0] 
			print "There are %s cities with 2 cubes, in:" % (totalfound)
			listc = findout1 [1]
			for a in listc:
				print a [0]
			listc = findout2 [1]
			for a in listc:
				print a [0]
			listc = findout3 [1]
			for a in listc:
				print a [0]
			listc = findout4 [1]
			for a in listc:
				print a [0]
			g.start () 
		else:
			print "Please answer 1,2,3 or 4."
			g.cube2info ()


	def cube1info (self):
		it = inaturn ()
		g = game ()
		print """What colour?
1. Blue
2. Yellow
3. Red
4. Black
5. All"""
		answer = raw_input ('>')
		if answer == '1':
			findout = it.getxcube ('ucube',1)
			print "There are %s cities with 1 blue cubes, in:" % (findout [0][0])
			listc = findout [1]
			for a in listc:
				print a [0]
			g.start () 
		elif answer == '2':
			findout = it.getxcube ('ycube',1)
			print "There are %s cities with 1 yellow cubes, in:" % (findout [0][0])
			listc = findout [1]
			for a in listc:
				print a [0]
			g.start () 
		elif answer == '3':
			findout = it.getxcube ('rcube',1)
			print "There are %s cities with 1 red cubes, in:" % (findout [0][0])
			listc = findout [1]
			for a in listc:
				print a [0]
			g.start () 
		elif answer == '4':
			findout = it.getxcube ('bcube',1)
			print "There are %s cities with 1 black cubes, in:" % (findout [0][0])
			listc = findout [1]
			for a in listc:
				print a [0]
			g.start () 
		elif answer == '5':
			findout1 = it.getxcube ('bcube',1)
			findout2 = it.getxcube ('ucube',1)
			findout3 = it.getxcube ('ycube',1)
			findout4 = it.getxcube ('rcube',1)
			totalfound =findout1 [0][0] + findout2 [0][0] + findout3 [0][0] + findout4 [0][0] 
			print "There are %s cities with 1 cubes, in:" % (totalfound)
			listc = findout1 [1]
			for a in listc:
				print a [0]
			listc = findout2 [1]
			for a in listc:
				print a [0]
			listc = findout3 [1]
			for a in listc:
				print a [0]
			listc = findout4 [1]
			for a in listc:
				print a [0]
			g.start () 
		else:
			print "Please answer 1,2,3 or 4."
			g.cube1info ()

	def playerlocinfo (self):
		g = game ()
		it = inaturn ()
		with sqlite3.connect('pandemic.db') as conn:
		   	cursor = conn.cursor()
			tobedone = """SELECT ap FROM gsTBL;"""
			cursor.execute (tobedone)
			answerX = cursor.fetchone ()
			location = it.getplayer (answerX [0])
			print "You, %s are located in %s" % (answerX[0],location)
			g.start ()

	def handinfo (self):
		g = game ()
		it = inaturn ()
		with sqlite3.connect('pandemic.db') as conn:
		   	cursor = conn.cursor()
			tobedone = """SELECT ap FROM gsTBL;"""
			cursor.execute (tobedone)
			answerX = cursor.fetchone ()
			hand = it.gethand (answerX [0])
			count = 0
			for a in hand:
				count = count + 1
			print "You, %s have the %s below cards in your hand:" % (answerX[0], count)
			for a in hand:
				print a [0]
			g.start ()
		
	def action (self):
		g = game ()
		it = inaturn ()
                print """What action would you like to take?
1- Take a train or ferry to another city (doesn't work correctly, you can move anywhere).
2- Play a card to take a direct flight to that city.
3- Play the card of the city you are in to take a charter flight to any location.
4- Take a shuttle flight from one research station to another.
5- Treat illness in your current city.
6- Play 5 city cards of the same colour to cure an disease. You must be in a research station.
7- Give another player a card from your hand that matches the city you are in if you are both in the same city.
8- Take a card from another player that matches the city you are in if you are both in the same city.
9- Build a research centre play the city card that matches the city you are in to build a research centre."""
                thing = raw_input ('>')
                if thing == '1':
                        g.mp ()
                elif thing == '2':
                        g.df ()
                elif thing == '3':
                        g.cf ()
                elif thing == '4':
                        g.sf ()
                elif thing == '5':
                        g.td ()
                elif thing == '6':
                        g.cd ()
                elif thing == '7':
                        g.skg ()
                elif thing == '8':
                        g.skt ()
                elif thing == '9':
                        g.br ()
		else:
			print "Please type a number from 1-9 for an action."
			game.action ()


	def mp (self):
		g=game ()
		it = inaturn ()
		pa = playeraction ()
		ap = it.getap ()
		location = it.getplayer (ap)
		print "Where would you like to go?"
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
	        	tobedone = """SELECT connect FROM BoardTBL WHERE name is '%s';""" % (location)
			cursor.execute( tobedone )
			answerX = cursor.fetchone ( )
			connect = int (answerX [0])
			t = 0
			timestodo = connect - 1
			while t <= timestodo:
				t = t + 1
				use = str (t)
				find = "co"+use
	        		tobedone = """SELECT %s FROM BoardTBL WHERE name is '%s';""" % (find,location)
				cursor.execute( tobedone )
				answerX = cursor.fetchone ( )
				connect = answerX [0]
				part1 = str (t) + '. '
				part2 = str (connect)
				print part1 + part2
		choice = raw_input ('>')
		if choice == '1':	
			cursor = conn.cursor()
	        	tobedone = """SELECT co1 FROM BoardTBL WHERE name is '%s';""" % (location)
			cursor.execute( tobedone )
			answerX = cursor.fetchone ( )
			destination = answerX [0]
		elif choice == '2':	
			cursor = conn.cursor()
	        	tobedone = """SELECT co2 FROM BoardTBL WHERE name is '%s';""" % (location)
			cursor.execute( tobedone )
			answerX = cursor.fetchone ( )
			destination = answerX [0]
		elif choice == '3':	
			cursor = conn.cursor()
	        	tobedone = """SELECT co3 FROM BoardTBL WHERE name is '%s';""" % (location)
			cursor.execute( tobedone )
			answerX = cursor.fetchone ( )
			destination = answerX [0]
		elif choice == '4':	
			cursor = conn.cursor()
	        	tobedone = """SELECT co4 FROM BoardTBL WHERE name is '%s';""" % (location)
			cursor.execute( tobedone )
			answerX = cursor.fetchone ( )
			destination = answerX [0]
		elif choice == '5':	
			cursor = conn.cursor()
	        	tobedone = """SELECT co5 FROM BoardTBL WHERE name is '%s';""" % (location)
			cursor.execute( tobedone )
			answerX = cursor.fetchone ( )
			destination = answerX [0]
		elif choice == '6':	
			cursor = conn.cursor()
	        	tobedone = """SELECT co6 FROM BoardTBL WHERE name is '%s';""" % (location)
			cursor.execute( tobedone )
			answerX = cursor.fetchone ( )
			destination = answerX [0]
		else:
			print "You must choose an option from the given selection"
			g.mp ()	
		pa.trainboat (ap,location,destination)
		g.start ()
		
	def df (self):
		g=game ()
		it = inaturn ()
		pa = playeraction ()
		ap = it.getap ()
		location = it.getplayer (ap)
		print "Where do you want to take a direct flight to?"
		hand = it.gethand (ap)
		t = 0
		for a in hand:
			t = t + 1
			card = str (a [0])
			op = str (t) + '. '
			print op + card
		choice = raw_input ('>')
		if choice == '1':
			pa.direct (ap,hand[0][0])
			g.start ()
		elif choice == '2':
			pa.direct (ap,hand[1][0])
			g.start ()
		elif choice == '3':
			pa.direct (ap,hand[2][0])
			g.start ()
		elif choice == '4':
			pa.direct (ap,hand[3][0])
			g.start ()
		elif choice == '5':
			pa.direct (ap,hand[4][0])
			g.start ()
		elif choice == '6':
			pa.direct (ap,hand[5][0])
			g.start ()
		elif choice == '7':
			pa.direct (ap,hand[6][0])
			g.start ()
		elif choice == '8':
			pa.direct (ap,hand[7][0])
			g.start ()
		elif choice == '9':
			pa.direct (ap,hand[4][0])
			g.start ()
		else:
			print "You must make a choice from the given options by entering a number."
			g.df ()

	def cf (self):
		g=game ()
		it = inaturn ()
		pa = playeraction ()
		ap = it.getap ()
		location = it.getplayer (ap)
		hand = it.gethand (ap)
		print "Which card will you play for the charter flight?This must match your current location or it won't work!"
		i = 0
		for a in hand:
			i = i +1
			opt = str (i) + '. '
			card = str (a [0])
			print opt + card
		answer = raw_input ('>')
		if answer == '1':
			card = hand [0][0]
		elif answer == '2':
			card = hand [1][0]
		elif answer == '3':
			card = hand [2][0]
		elif answer == '4':
			card = hand [3][0]
		elif answer == '5':
			card = hand [4][0]
		elif answer == '6':
			card = hand [5][0]
		elif answer == '7':
			card = hand [6][0]
		elif answer == '8':
			card = hand [7][0]
		elif answer == '9':
			card = hand [8][0]

		print "Using %s" % card

		print "Where do you want to take a charter flight to?"
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = """SELECT name FROM BoardTBL;"""
			cursor.execute (tobedone)
			answerX = cursor.fetchall ()
			i = 0
			print "The possible destination cities are listed below. Choose a number from below"
			for a in answerX:
				i = i +1
				opt = str (i) + '. '
				country = str (a [0])
				print opt + country
		answer = raw_input ('>')
		if answer == '1':
			pa.charter (ap,card,answerX[0][0])
		elif answer == '2':
			pa.charter (ap,card,answerX[1][0])
		elif answer == '3':
			pa.charter (ap,card,answerX[2][0])
		elif answer == '4':
			pa.charter (ap,card,answerX[3][0])
		elif answer == '5':
			pa.charter (ap,card,answerX[4][0])
		elif answer == '6':
			pa.charter (ap,card,answerX[5][0])
		elif answer == '7':
			pa.charter (ap,card,answerX[6][0])
		elif answer == '8':
			pa.charter (ap,card,answerX[7][0])
		elif answer == '9':
			pa.charter (ap,card,answerX[8][0])
		elif answer == '10':
			pa.charter (ap,card,answerX[9][0])
		elif answer == '11':
			pa.charter (ap,card,answerX[10][0])
		elif answer == '12':
			pa.charter (ap,card,answerX[11][0])
		elif answer == '13':
			pa.charter (ap,card,answerX[12][0])
		elif answer == '14':
			pa.charter (ap,card,answerX[13][0])
		elif answer == '15':
			pa.charter (ap,card,answerX[14][0])
		elif answer == '16':
			pa.charter (ap,card,answerX[15][0])
		elif answer == '17':
			pa.charter (ap,card,answerX[16][0])
		elif answer == '18':
			pa.charter (ap,card,answerX[17][0])
		elif answer == '19':
			pa.charter (ap,card,answerX[18][0])
		elif answer == '20':
			pa.charter (ap,card,answerX[19][0])
		elif answer == '21':
			pa.charter (ap,card,answerX[20][0])
		elif answer == '22':
			pa.charter (ap,card,answerX[21][0])
		elif answer == '23':
			pa.charter (ap,card,answerX[22][0])
		elif answer == '24':
			pa.charter (ap,card,answerX[23][0])
		elif answer == '25':
			pa.charter (ap,card,answerX[24][0])
		elif answer == '26':
			pa.charter (ap,card,answerX[25][0])
		elif answer == '27':
			pa.charter (ap,card,answerX[26][0])
		elif answer == '28':
			pa.charter (ap,card,answerX[27][0])
		elif answer == '29':
			pa.charter (ap,card,answerX[28][0])
		elif answer == '30':
			pa.charter (ap,card,answerX[29][0])
		elif answer == '31':
			pa.charter (ap,card,answerX[30][0])
		elif answer == '32':
			pa.charter (ap,card,answerX[31][0])
		elif answer == '33':
			pa.charter (ap,card,answerX[32][0])
		elif answer == '34':
			pa.charter (ap,card,answerX[33][0])
		elif answer == '35':
			pa.charter (ap,card,answerX[34][0])
		elif answer == '36':
			pa.charter (ap,card,answerX[35][0])
		elif answer == '37':
			pa.charter (ap,card,answerX[36][0])
		elif answer == '38':
			pa.charter (ap,card,answerX[37][0])
		elif answer == '39':
			pa.charter (ap,card,answerX[38][0])
		elif answer == '40':
			pa.charter (ap,card,answerX[39][0])
		elif answer == '41':
			pa.charter (ap,card,answerX[40][0])
		elif answer == '42':
			pa.charter (ap,card,answerX[41][0])
		elif answer == '43':
			pa.charter (ap,card,answerX[42][0])
		elif answer == '44':
			pa.charter (ap,card,answerX[43][0])
		elif answer == '45':
			pa.charter (ap,card,answerX[44][0])
		elif answer == '46':
			pa.charter (ap,card,answerX[45][0])
		elif answer == '47':
			pa.charter (ap,card,answerX[46][0])
		elif answer == '48':
			pa.charter (ap,card,answerX[47][0])
		elif answer == '49':
			pa.charter (ap,card,answerX[48][0])
		elif answer == '50':
			pa.charter (ap,card,answerX[49][0])
		elif answer == '51':
			pa.charter (ap,card,answerX[50][0])
		else:
			print "You must choose a valid option"
			g.start ()
		g.start ()

	def sf (sel):
		g=game ()
		it = inaturn ()
		pa = playeraction ()
		ap = it.getap ()
		location = it.getplayer (ap)
		with sqlite3.connect('pandemic.db') as conn:
			cursor = conn.cursor()
			tobedone = """SELECT name FROM BoardTBL where rstation = 1;"""
			cursor.execute (tobedone)
			answerX = cursor.fetchall ()
			rstationloc = 0
			for a in answerX:
				if a[0] == location:
					rstationloc = 1
			if rstationloc == 0:
				print "Your location %s, has no research station to take a shuttle flight from" % (location)
				g.start ()
			if rstationloc == 1:
				print "Where would you like to take a shuttle flight to?"
				i = 0
				for a in answerX:
					i = i + 1
					opt = str (i) + '. '
					print opt + a[0]
		answer = raw_input ('>')
		if answer == '1':
			pa.shuttle (ap,answerX[0][0])
		elif answer == '2':
			pa.shuttle (ap,answerX[1][0])
		elif answer == '3':
			pa.shuttle (ap,answerX[2][0])
		elif answer == '4':
			pa.shuttle (ap,answerX[3][0])
		elif answer == '5':
			pa.shuttle (ap,answerX[4][0])
		elif answer == '6':
			pa.shuttle (ap,answerX[5][0])
		elif answer == '7':
			pa.shuttle (ap,answerX[6][0])
		elif answer == '8':
			pa.shuttle (ap,answerX[7][0])
		elif answer == '9':
			pa.shuttle (ap,answerX[8][0])
		elif answer == '10':
			pa.shuttle (ap,answerX[9][0])
		elif answer == '11':
			pa.shuttle (ap,answerX[10][0])
		elif answer == '12':
			pa.shuttle (ap,answerX[11][0])
		else:
			print "You must choose a valid option"
			g.start ()
		g.start ()
				
	def td (self):
		g=game ()
		it = inaturn ()
		pa = playeraction ()
		ap = it.getap ()
		location = it.getplayer (ap)
		print """What colour cube would you like to remove?
1. Red
2. Blue
3. Yellow
4. Black"""
		answer = raw_input ('>')
		if answer == '1':
			col = 'rcube'
			cubes = it.getcitycubes ('rcube',location)

		elif answer == '2':
			col = 'ucube'
			cubes = it.getcitycubes ('ucube',location)

		elif answer == '3':
			col = 'ycube'
			cubes = it.getcitycubes ('ycube',location)

		elif answer == '4':
			col = 'bcube'
			cubes = it.getcitycubes ('bcube',location)
		else:
			print "You must choose 1,2,3 or 4."
			g.start ()

		if cubes > 0:
			pa.treat (ap,col)
			print "Removing a cube of the chosen colour from %s" % (location) 
		else:
			print "There are no cubes of that colour in %s." % (location)
		g.start ()
					



#	def cd (self):
#	def skg (self):
#	def skt (self):
#	def br (self):

	def gameover (self):
		print "The game is over"
		sys.exit()
		
