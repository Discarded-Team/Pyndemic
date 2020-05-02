# coding: utf-8
import logging

from .exceptions import GameCrisisException


class NoHealthException(GameCrisisException):
    def __init__(self, colour):
        self.colour = colour

    def __str__(self):
        return f'Public health resistance vs {self.colour} disease is no more! Pandemics!'


class Disease:
    """
        Monitors public health resistance vs this disease and whether the disease was cured completely
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

        assert isinstance(change_size, int)
        self.public_health += change_size

        logging.debug(
            (f'Public health resistance vs {self.colour} disease is now '
             f'{self.public_health}.'))

    def decrease_resistance(self, change_size):
        """
        :param change_size: Int
        """

        assert isinstance(change_size, int)
        if change_size >= self.public_health:
            raise NoHealthException(self.colour)
        else:
            self.public_health -= change_size

            logging.debug(
                (f'Public health resistance vs {self.colour} disease is now '
                 f'{self.public_health}.'))
