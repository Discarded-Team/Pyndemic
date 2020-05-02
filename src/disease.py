# coding: utf-8
import logging

from .exceptions import GameCrisisException


class NullDiseaseCapacityException(GameCrisisException):
    def __init__(self, colour):
        self.colour = colour

    def __str__(self):
        return f'No {self.colour} disease cubes left!'


class Disease:
    """
        Monitors disease cubes in bank and whether it was cured completely
        :param colour: Str
        :param cubes_at_bank: Int
        """

    def __init__(self, colour, cubes_at_bank):
        self.colour = colour
        self.cured = False
        self.cubes_at_bank = cubes_at_bank

    def __str__(self):
        result = f'{self.colour} disease'
        if self.cured:
            result += ' (cured)'

        return result

    def put_cubes_to_bank(self, qty_of_cubes):
        """
        :param qty_of_cubes: Int
        """

        assert isinstance(qty_of_cubes, int)
        self.cubes_at_bank += qty_of_cubes

        logging.debug(
            (f'{self.colour} disease capacity is now '
             f'{self.cubes_at_bank}.'))

    def take_cubes_from_bank(self, qty_of_cubes):
        """
        :param qty_of_cubes: Int
        """

        assert isinstance(qty_of_cubes, int)
        if qty_of_cubes >= self.cubes_at_bank:
            raise NullDiseaseCapacityException(self.colour)
        else:
            self.cubes_at_bank -= qty_of_cubes

            logging.debug(
                (f'{self.colour} disease capacity is now '
                 f'{self.cubes_at_bank}.'))
