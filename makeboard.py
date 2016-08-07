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
			"NoConnect",
			"NaConnect");'''
			cursor.execute( tobedone )
			conn.commit()
		


