# coding: utf-8
import random
from itertools import cycle, chain

from card import Card


class Deck:
    def __init__(self):
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

    def get_discard_count(self):
        return len(self.discard)

    # TODO: make DiseaseDeck subclass and place this method there
    def shuffle_discard_to_top(self):
        random.shuffle(self.discard)
        self.cards = self.discard + self.cards
        self.discard = []

    def shuffle(self):
        random.shuffle(self.cards)

    # TODO: make PlayerDeck subclass and place this method there
    def add_epidemics(self, number_epidemics):
        card_piles = [[] for i in range(number_epidemics)]
        random.shuffle(self.cards)

        for pile in cycle(card_piles):
            pile.append(self.cards.pop())
            if not self.cards:
                break

        for pile in card_piles:
            epidemic_card = Card("Epidemic", "All")
            place_to_insert = random.randint(0, len(pile))
            pile.insert(place_to_insert, epidemic_card)

        self.cards = list(chain(*card_piles))

