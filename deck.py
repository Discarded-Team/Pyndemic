# coding: utf-8
import random
from itertools import cycle, chain

import config
from card import PlayerCard, InfectCard


class Deck:
    def __init__(self):
        self.cards = []
        self.discard = []

    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)

    def __str__(self):
        return '{} (deck size: {}, discard size: {})'.format(
            self.__class__.__name__, len(self.cards), len(self.discard))

    def prepare(self, settings):
        self.cards = []
        self.discard = []

    def take_top_card(self):
        return self.cards.pop(0)

    def take_bottom_card(self):
        return self.cards.pop()

    def add_card(self, new_card):
        self.cards.append(new_card)

    def add_discard(self, discarded_card):
        self.discard.append(discarded_card)

    def shuffle(self):
        random.shuffle(self.cards)


class PlayerDeck(Deck):
    def prepare(self, settings):
        super().prepare(settings)

        cities_section = settings['Cities']
        city_colours_section = settings['City Colours']

        for city_id in cities_section:
            city_name = cities_section[city_id]
            city_colour = city_colours_section[city_id]
            new_card = PlayerCard(city_name, city_colour)
            self.add_card(new_card)

        # TODO: add action cards

    def add_epidemics(self, number_epidemics):
        card_piles = [[] for i in range(number_epidemics)]
        random.shuffle(self.cards)

        for pile in cycle(card_piles):
            pile.append(self.cards.pop())
            if not self.cards:
                break

        for pile in card_piles:
            epidemic_card = PlayerCard('Epidemic', 'no-colour')
            place_to_insert = random.randint(0, len(pile))
            pile.insert(place_to_insert, epidemic_card)

        self.cards = list(chain(*card_piles))


class InfectDeck(Deck):
    def prepare(self, settings):
        super().prepare(settings)

        cities_section = settings['Cities']
        city_colours_section = settings['City Colours']

        for city_id in cities_section:
            city_name = cities_section[city_id]
            city_colour = city_colours_section[city_id]
            new_card = InfectCard(city_name, city_colour)
            self.add_card(new_card)

    def shuffle_discard_to_top(self):
        random.shuffle(self.discard)
        self.cards = self.discard + self.cards
        self.discard = []

