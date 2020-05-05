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
        cube_colours = ['Red', 'Yellow']
        self.city.init_colours(cube_colours)
        self.assertEqual(0, self.city.infection_levels['Red'])
        self.assertEqual(0, self.city.infection_levels['Yellow'])

    def add_cube(self, colour):
        self.city.infection_levels['Black'] = 2
        self.city.add_cube('Black')
        self.assertEqual(3, self.city.infection_levels['Black'])

    def test_remove_cube(self):
        self.city.infection_levels['Black'] = 2
        self.city.remove_cube('Black')
        self.assertEqual(1, self.city.infection_levels['Black'])

        self.city.infection_levels['Black'] = 0
        with self.assertRaises(GameException):
            self.city.remove_cube('Black')
        self.assertEqual(0, self.city.infection_levels['Black'])

    def test_remove_all_cubes(self):
        self.city.infection_levels['Red'] = 3
        dropped_cubes = self.city.remove_all_cubes('Red')
        self.assertEqual(3, dropped_cubes)
        self.assertEqual(0, self.city.infection_levels['Red'])

        with self.assertRaises(GameException):
            self.city.remove_all_cubes('Red')
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

    def test_get_max_cubes(self):
        self.city.infection_levels['Blue'] = 1
        self.city.infection_levels['Red'] = 2
        self.city.infection_levels['Yellow'] = 4
        self.assertEqual(4, self.city.get_max_cubes())

    def test_get_cubes(self):
        self.city.infection_levels['Blue'] = 2
        self.assertEqual(2, self.city.infection_levels['Blue'])

