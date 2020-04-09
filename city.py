# coding: utf-8
from configparser import ConfigParser


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

    def init_city_colours(self, cube_colours):
        for colour in cube_colours:
            self.cubes[colour] = 0

    def remove_cube(self, colour):
        # TODO: check for positive values (and where we actually must do this)
        self.cubes[colour] -= 1

    def add_cube(self, colour):
        self.cubes[colour] += 1

    def build_lab(self):
        if self.has_lab:
            return False
        self.has_lab = True
        return True

    def add_connection(self, new_city):
        self.connected_cities.append(new_city)

    def remove_all_cubes(self, colour):
        self.cubes[colour] = 0

    def get_max_cubes(self):
        return max(self.cubes.values())

    # TODO: redesign this method
    @classmethod
    def set_cube_colours(cls, settings):
        cls.cube_colours = settings['Colours'].get('colours').split(',')

