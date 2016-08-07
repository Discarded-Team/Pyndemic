#!/usr/bin/env python
# vim: tabstop=4 softtabstop=4 shiftwidth=4 smarttab expandtab:

import unittest
from makeboard import startinggame

global nocountries

class T( unittest.TestCase ):

# This def should test if the createcountry
	def test_setup (self):
		nocountries = 'thewrongnumber'
		sg = startinggame ()
		sg.setup (nocountries)
		self.assertEqual(nocountries,0, msg = 'number of countries is not correct')

