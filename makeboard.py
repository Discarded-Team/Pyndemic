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
			infectfile = open(infect,'r') 
			for line in infectfile:
				with sqlite3.connect('pandemic.db') as conn:
		            		tobedone = """INSERT INTO idTBL (name) select name from BoardTBL;""" 
		            		cursor.execute( tobedone )
					conn.commit()
		            		tobedone = """UPDATE idTBL SET pos = 0;""" 
		            		cursor.execute( tobedone )
					conn.commit()

# This sets up the infection deck discard pile
	def iddTBL (self,infect):
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
			
		
