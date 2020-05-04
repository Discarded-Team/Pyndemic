# coding: utf-8
import logging

from .exceptions import GameCrisisException


class NoHealthException(GameCrisisException):
    def __init__(self, colour):
        self.colour = colour

    def __str__(self):
        return f'Public health resistance to {self.colour} disease is over! Pandemic!'


class Disease:
    """
        Monitors public health resistance to this disease and whether the disease has been cured completely
        :param colour: Str
        :param init_public_health: Int
        """

    def __init__(self, colour, init_public_health):
        self.colour = colour
        self.cured = False
        self.public_health = init_public_health

    def __str__(self):
        result = f'{self.colour} disease'
        if self.cured:
            result += ' (cured)'

        return result

    def increase_resistance(self, change_size):
        """
        :param change_size: Int
        """

        self.public_health += change_size

        logging.debug(
            (f'Public health resistance to {self.colour} disease is now '
             f'{self.public_health}.'))

    def decrease_resistance(self, change_size):
        """
        :param change_size: Int
        """

        if change_size >= self.public_health:
            raise NoHealthException(self.colour)
        else:
            self.public_health -= change_size

            logging.debug(
                (f'Public health resistance to {self.colour} disease is now '
                 f'{self.public_health}.'))
