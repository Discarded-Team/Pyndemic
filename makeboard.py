#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

import sqlite3

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
	def pdTBL (self,player):
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
			playerfile = open(player,'r') 
			for line in playerfile:
				with sqlite3.connect('pandemic.db') as conn:
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
