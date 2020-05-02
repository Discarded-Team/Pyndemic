# coding: utf-8


class Card:
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

    def __str__(self):
        return f'Card "{self.name}-{self.colour}"'


class PlayerCard(Card):
    pass


class InfectCard(Card):
    pass
