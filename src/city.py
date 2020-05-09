# coding: utf-8
import logging

from .exceptions import GameException


class NoDiseaseInCityException(GameException):
    def __init__(self, city, colour):
        self.city = city
        self.colour = colour

    def __str__(self):
        return f'No {self.colour} disease found in {self.city.name}!'


class City:
    def __init__(self, name, colour):
        self.name = name
        self.has_lab = False
        self.colour = colour
        self.infection_levels = {}
        self.distance = 999 # TODO unused?
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

    def init_colours(self, disease_colours):
        for colour in disease_colours:
            self.infection_levels[colour] = 0

    def decrease_infection_level(self, colour):
        if not self.infection_levels[colour]:
            raise NoDiseaseInCityException(self, colour)
        self.infection_levels[colour] -= 1
        logging.debug(
            f'{colour} disease infection in {self} went one level down')

    def increase_infection_level(self, colour):
        self.infection_levels[colour] += 1
        logging.debug(
            f'{colour} disease infection in {self} went one level up')

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
    def nullify_infection_level(self, colour):
        if not self.infection_levels[colour]:
            raise NoDiseaseInCityException(self, colour)
        level_reduction = self.infection_levels[colour]
        self.infection_levels[colour] = 0
        logging.debug(
            f'{colour} disease infection in {self} dropped to zero level')

        return level_reduction

