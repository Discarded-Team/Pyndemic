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

    # TODO: rewrite or remove this method
    def get_connected_city(self, connection):
        return self.connected_cities[connection - 1]

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

    # TODO: remove this method after checking all places that use it
    def get_connections(self):
        return self.connected_cities

    def remove_all_cubes(self, colour):
        self.cubes[colour] = 0

    def get_max_cubes(self):
        return max(self.cubes.values())

    def get_cubes(self, colour):
        return self.cubes[colour]

    @classmethod
    def set_cube_colours(cls, settings_location):
        parser = ConfigParser()
        parser.read(settings_location)
        cls.cube_colours = parser.get('Colours', 'colours').split(',')

