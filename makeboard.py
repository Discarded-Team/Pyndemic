#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

import sqlite3

class startinggame:
	def BoardTBL (self,board):
		print "creating table of BoardTBL"
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
			print "created table"
			boardfile = open(board,'r') 
			for line in boardfile:
				with sqlite3.connect('pandemic.db') as conn:
			        	cursor = conn.cursor()
					print "adding data"
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
					print tobedone
		            		cursor.execute( tobedone )
					conn.commit()

	def setupresearch (self):
		with sqlite3.connect('pandemic.db') as conn:
			        cursor = conn.cursor()
		            	tobedone = """ALTER TABLE countries ADD COLUMN research;"""
		            	cursor.execute( tobedone )
				conn.commit()
				tobedone = """UPDATE countries SET research = 1 WHERE name is 'Atlanta'""";
		            	cursor.execute( tobedone )
				conn.commit()

	def setupcubes (self):
		with sqlite3.connect('pandemic.db') as conn:
			        cursor = conn.cursor()
		            	tobedone = """DROP TABLE IF EXISTS cubes;"""
		            	cursor.execute( tobedone )
				conn.commit()
				tobedone = """CREATE TABLE cubes ('col' TEXT,'nocubes'NUM);""";
		            	cursor.execute( tobedone )
				conn.commit()

		            	tobedone = """INSERT INTO cubes (col,nocubes) VALUES ('Red','20');"""
		            	cursor.execute( tobedone )
				conn.commit()

		            	tobedone = """INSERT INTO cubes (col,nocubes) VALUES ('Blue','20');"""
		            	cursor.execute( tobedone )
				conn.commit()

		            	tobedone = """INSERT INTO cubes (col,nocubes) VALUES ('Yellow','20');"""
		            	cursor.execute( tobedone )
				conn.commit()

		            	tobedone = """INSERT INTO cubes (col,nocubes) VALUES ('Black','20');"""
		            	cursor.execute( tobedone )
				conn.commit()

	def setupplayerdeck (self,board):
    		sg = startinggame ()
    		sg.setup ( )
    		sg.setupboard (board)
		with sqlite3.connect('pandemic.db') as conn:
			        cursor = conn.cursor()
		            	tobedone = """DROP TABLE IF EXISTS playerdeck;"""
		            	cursor.execute( tobedone )
				conn.commit()
				tobedone = """CREATE TABLE playerdeck ('card' TEXT);"""
		            	cursor.execute( tobedone )
				conn.commit()
		            	tobedone = """INSERT INTO playerdeck (card) SELECT name FROM countries;"""
				cursor.execute( tobedone )
				conn.commit()
