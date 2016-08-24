#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

import sqlite3
import random

# This creates and populates the table which contains the information from the game board.
class startinggame:
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
	def pddTBL (self,player):
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
	def idTBL (self,infect):
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
			"pos");'''
			cursor.execute( tobedone )
			conn.commit()
			characterfile = open(character,'r') 
			for line in characterfile:
				with sqlite3.connect('pandemic.db') as conn:
		            		tobedone = """INSERT INTO cTBL (name,pos) VALUES (%s);""" % (line)
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
			npile = thingy / nep
			numberofcardsinapile = int(npile)
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
			

class inaturn:
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


#	        	tobedone = 'INSERT INTO player3TBL (name) select name from shufpd ORDER BY pos DESC limit 3;'
#	       		     	cursor.execute( tobedone )
#		        	tobedone = 'SELECT pos FROM shufpd ORDER BY pos DESC limit 3;'
#	       		     	cursor.execute( tobedone )
#				conn.commit()
#				answerX = cursor.fetchall ( )
#				answer1 = answerX [3]
#				funny1 = answer1 [0]
#		        	tobedone = """DELETE FROM shufpd WHERE pos >= %s;""" % (funny1)
#	       		     	cursor.execute( tobedone )
#				conn.commit()

