#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

import sqlite3

class startinggame:
	def setup (self):
		print "creating table of countries"
		with sqlite3.connect('pandemic.db') as conn:
	            	cursor = conn.cursor()
	            	tobedone = 'DROP TABLE if exists countries;'
	            	cursor.execute( tobedone )
			conn.commit()
			tobedone = '''CREATE TABLE countries(
			"Name",
			"Co1",
			"Co2",
			"Co3",		
			"Co4",
			"Co5",
			"Co6",
			"co7",
			"co8",
			"co9",
			"co10",
			"co11",
			"co12",
			"co13",
			"co14",
			"co15",
			"co16",
			"co17",
			"co18",
			"co19",
			"co20",
			"co21",
			"co22",
			"co23",
			"co24",
			"co25",
			"co26",
			"co27",
			"co28",
			"co29",
			"co30",
			"co31",
			"co32",
			"co33",
			"co34",
			"co35",
			"co36",
			"co37",
			"co38",
			"co39",
			"co40",
			"co41",
			"co42",
			"co43",
			"co44",
			"co45",
			"co46",
			"co47",
			"co48");'''
			cursor.execute( tobedone )
			conn.commit()
		
	def setupboard (self,board):
		boardfile = open(board,'r') 
		for line in boardfile:
			with sqlite3.connect('pandemic.db') as conn:
			        cursor = conn.cursor()
		            	tobedone = """INSERT INTO countries ("Name",
			"Co1",
			"Co2",
			"Co3",		
			"Co4",
			"Co5",
			"Co6",
			"co7",
			"co8",
			"co9",
			"co10",
			"co11",
			"co12",
			"co13",
			"co14",
			"co15",
			"co16",
			"co17",
			"co18",
			"co19",
			"co20",
			"co21",
			"co22",
			"co23",
			"co24",
			"co25",
			"co26",
			"co27",
			"co28",
			"co29",
			"co30",
			"co31",
			"co32",
			"co33",
			"co34",
			"co35",
			"co36",
			"co37",
			"co38",
			"co39",
			"co40",
			"co41",
			"co42",
			"co43",
			"co44",
			"co45",	
			"co46",
			"co47",
			"co48") VALUES (%s);""" % (line)
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
