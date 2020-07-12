import random
from itertools import cycle, chain
import logging

from .exceptions import GameCrisisException
from .core import GameEntity
from .action_card import ACTION_CARDS
from .card import CityCard, InfectCard, EpidemicCard


class ExhaustedPlayerDeckException(GameCrisisException):
    def __str__(self):
        return 'Player deck exhausted!'


class Deck(GameEntity):
    def __init__(self):
        self.cards = []
        self.discard = []

    def __str__(self):
        return f'{self.__class__.__name__}'

    def info(self):
        result = (f'{self.__class__.__name__} (deck size: {len(self.cards)}, '
                  f'discard size: {len(self.discard)})')
        return result

    def clear(self):
        self.cards = []
        self.discard = []

    def take_top_card(self):
        return self.cards.pop(0)

    def take_bottom_card(self):
        return self.cards.pop()

    def add_card(self, new_card):
        self.cards.append(new_card)

    def add_discard(self, discarded_card, *, on_discard=True):
        if on_discard:
            discarded_card.on_discard()
        self.discard.append(discarded_card)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self, drawing_character, *, on_draw=True):
        """Draws a card from the deck.
        If `on_draw` parameter is set to False, the card object will not
        perform its on-draw action.
        """
        try:
            drawn_card = self.take_top_card()
        except IndexError:
            return self.on_deck_exhausted(drawing_character)

        if on_draw:
            drawn_card.on_draw(drawing_character)
        return drawn_card

    def on_deck_exhausted(self, drawing_character):
        return None


class PlayerDeck(Deck):
    def prepare(self, cities):
        self.clear()
        for city in cities:
            new_card = CityCard(city.name, city.colour)
            self.add_card(new_card)

        for card_class in ACTION_CARDS:
            # TODO: somehow get the settings which cards to include
            new_card = card_class()
            self.add_card(new_card)

        logging.debug(
            f'{self} prepared.')

    def add_epidemics(self, number_epidemics):
        card_piles = [[] for i in range(number_epidemics)]
        random.shuffle(self.cards)

        for pile in cycle(card_piles):
            pile.append(self.cards.pop())
            if not self.cards:
                break

        for pile in card_piles:
            epidemic_card = EpidemicCard()
            place_to_insert = random.randint(0, len(pile))
            pile.insert(place_to_insert, epidemic_card)

        self.cards = list(chain(*card_piles))
        logging.debug(
            f'Added {number_epidemics} Epidemics to {self}.')

    def on_deck_exhausted(self, drawing_character):
        raise ExhaustedPlayerDeckException


class InfectDeck(Deck):
    def prepare(self, cities):
        self.clear()
        for city in cities:
            new_card = InfectCard(city.name, city.colour)
            self.add_card(new_card)

        logging.debug(
            f'{self} prepared.')

    def shuffle_discard_to_top(self):
        random.shuffle(self.discard)
        self.cards = self.discard + self.cards
        self.discard = []
        logging.debug(
            f'Shuffled infect discard and placed on top of {self}.')
