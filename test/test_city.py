# coding: utf-8
import unittest
from unittest import TestCase, skip, expectedFailure

import os.path as op
import random

from src.exceptions import *
from src.city import City


class CityTestCase(TestCase):
    def setUp(self):
        self.city = City('London', 'Blue')

    def test_init(self):
        city = City('London', 'Blue')
        self.assertEqual('London', city.name)
        self.assertEqual('Blue', city.colour)
        self.assertFalse(city.has_lab)

    def test_init_city_colours(self):
        self.city.infection_levels = {}
        disease_colours = ['Red', 'Yellow']
        self.city.init_colours(disease_colours)
        self.assertEqual(0, self.city.infection_levels['Red'])
        self.assertEqual(0, self.city.infection_levels['Yellow'])

    def test_increase_infection_level(self):
        self.city.infection_levels['Black'] = 2
        self.city.increase_infection_level('Black')
        self.assertEqual(3, self.city.infection_levels['Black'])

    def test_decrease_infection_level(self):
        self.city.infection_levels['Black'] = 2
        self.city.decrease_infection_level('Black')
        self.assertEqual(1, self.city.infection_levels['Black'])

        self.city.infection_levels['Black'] = 0
        with self.assertRaises(GameException):
            self.city.decrease_infection_level('Black')
        self.assertEqual(0, self.city.infection_levels['Black'])

    def test_nullify_infection_level(self):
        self.city.infection_levels['Red'] = 3
        level_reduction = self.city.nullify_infection_level('Red')
        self.assertEqual(3, level_reduction)
        self.assertEqual(0, self.city.infection_levels['Red'])

        with self.assertRaises(GameException):
            self.city.nullify_infection_level('Red')
        self.assertEqual(0, self.city.infection_levels['Red'])

    def test_build_lab(self):
        success = self.city.build_lab()
        self.assertTrue(success)
        self.assertTrue(self.city.has_lab)

        success = self.city.build_lab()
        self.assertFalse(success)
        self.assertTrue(self.city.has_lab)

    def test_add_connection(self):
        another_city = City('New York', 'Yellow')
        self.city.add_connection(another_city)
        self.assertIn(another_city, self.city.connected_cities)

