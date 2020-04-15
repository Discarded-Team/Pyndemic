# coding: utf-8


class Disease:
    def __init__(self, colour):
        self.colour = colour
        self.cured = False

    def __repr__(self):
        return '{}({!r})'.format(
            self.__class__.__name__, self.colour)

    def __str__(self):
        result = '{} disease'.format(self.colour)
        if self.cured:
            result += ' (cured)'

        return result

