# coding: utf-8
import logging

from .exceptions import GameException


class NoCityCubesException(GameException):
    def __init__(self, city, colour):
        self.city = city
        self.colour = colour

    def __str__(self):
        return f'No {self.colour} cubes left in {self.city.name}!'


class City:
    cube_colours = []

    def __init__(self, name, colour):
        self.name = name
        self.has_lab = False
        self.colour = colour
        self.cubes = {}
        self.init_city_colours(__class__.cube_colours)
        self.distance = 999
        self.connected_cities = []
        logging.debug(
            f'Created location {self}')

    def __str__(self):
        return f'City {self.name} ({self.colour})'

    def info(self):
        has_lab = 'built' if self.has_lab else 'not built'
        result = (f'City {self.name} (colour: {self.colour}, total neighbours:'
                  f' {len(self.connected_cities)}, laboratory: {has_lab})')

        return result

    def init_city_colours(self, cube_colours):
        for colour in cube_colours:
            self.cubes[colour] = 0

    def remove_cube(self, colour):
        if not self.cubes[colour]:
            raise NoCityCubesException(self, colour)
        self.cubes[colour] -= 1
        logging.debug(
            f'Removed {colour} cube from {self}')

    def add_cube(self, colour):
        self.cubes[colour] += 1
        logging.debug(
            f'Added {colour} cube to {self}')

    def build_lab(self):
        if self.has_lab:
            return False
        self.has_lab = True
        logging.debug(
            f'Built laboratory in {self}')

        return True

    def add_connection(self, new_city):
        self.connected_cities.append(new_city)

    # TODO redesign this method
    def remove_all_cubes(self, colour):
        if not self.cubes[colour]:
            raise NoCityCubesException(self, colour)
        dropped_cubes = self.cubes[colour]
        self.cubes[colour] = 0
        logging.debug(
            f'Removed all {colour} cubes from {self}')

        return dropped_cubes

    def get_max_cubes(self):
        return max(self.cubes.values())

    # TODO: redesign this method
    @classmethod
    def set_cube_colours(cls, settings):
        cls.cube_colours = settings['Colours'].get('colours').split(',')

