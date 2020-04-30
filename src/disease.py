# coding: utf-8


class Disease:
    def __init__(self, colour):
        self.colour = colour
        self.cured = False

    def __str__(self):
        result = f'{self.colour} disease'
        if self.cured:
            result += ' (cured)'

        return result

