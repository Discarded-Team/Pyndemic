# coding: utf-8
import unittest
from unittest import TestCase, skip, expectedFailure

import os.path as op
import random

from src.exceptions import *
from src.city import City


class CityClassmethodTestCase(TestCase):
    def test_set_cube_colours(self):
        saved = City.cube_colours

        City.cube_colours = []
        mocked_settings = {'Colours': {'colours': 'Red,Blue,Yellow,Black'}}
        City.set_cube_colours(mocked_settings)
        self.assertIn('Yellow', City.cube_colours)
        self.assertIn('Red', City.cube_colours)

        City.cube_colours = saved


class CityTestCase(TestCase):
    def setUp(self):
        self.city = City('London', 'Blue')

    def test_init(self):
        city = City('London', 'Blue')
        self.assertEqual('London', city.name)
        self.assertEqual('Blue', city.colour)
        self.assertFalse(city.has_lab)

    def test_init_city_colours(self):
        self.city.cubes = {}
        cube_colours = ['Red', 'Yellow']
        self.city.init_city_colours(cube_colours)
        self.assertEqual(0, self.city.cubes['Red'])
        self.assertEqual(0, self.city.cubes['Yellow'])

    def add_cube(self, colour):
        self.city.cubes['Black'] = 2
        self.city.add_cube('Black')
        self.assertEqual(3, self.city.cubes['Black'])

    def test_remove_cube(self):
        self.city.cubes['Black'] = 2
        self.city.remove_cube('Black')
        self.assertEqual(1, self.city.cubes['Black'])

        self.city.cubes['Black'] = 0
        with self.assertRaises(GameException):
            self.city.remove_cube('Black')
        self.assertEqual(0, self.city.cubes['Black'])

    def test_remove_all_cubes(self):
        self.city.cubes['Red'] = 3
        dropped_cubes = self.city.remove_all_cubes('Red')
        self.assertEqual(3, dropped_cubes)
        self.assertEqual(0, self.city.cubes['Red'])

        with self.assertRaises(GameException):
            self.city.remove_all_cubes('Red')
        self.assertEqual(0, self.city.cubes['Red'])

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
        self.city.cubes['Blue'] = 1
        self.city.cubes['Red'] = 2
        self.city.cubes['Yellow'] = 4
        self.assertEqual(4, self.city.get_max_cubes())

    def test_get_cubes(self):
        self.city.cubes['Blue'] = 2
        self.assertEqual(2, self.city.cubes['Blue'])

