# coding: utf-8


class Card:
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

    def __repr__(self):
        return '{}({!r}, {!r})'.format(
            self.__class__.__name__, self.name, self.colour)


class PlayerCard(Card):
    pass


class InfectCard(Card):
    pass
