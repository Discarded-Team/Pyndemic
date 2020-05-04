# coding: utf-8
import unittest
from unittest import TestCase, skip, expectedFailure

import random

from src.city import City
from src.card import Card, PlayerCard, InfectCard
from src.deck import Deck, PlayerDeck, InfectDeck


class DeckTestCase(TestCase):
    def setUp(self):
        self.deck = Deck()
        self.test_cards = [
            Card('London', 'Blue'),
            Card('Washington', 'Yellow'),
            Card('Bejing', 'Red'),
            Card('Moscow', 'Black'),
            Card('New York', 'Yellow'),
        ]
        self.deck.cards = self.test_cards.copy()

    def test_clear(self):
        self.deck.clear()
        self.assertEqual([], self.deck.cards)
        self.assertEqual([], self.deck.discard)

    def test_take_top_card(self):
        card = self.deck.take_top_card()
        self.assertEqual('London', card.name)

        next_card = self.deck.take_top_card()
        self.assertEqual('Yellow', next_card.colour)

    def test_take_bottom_card(self):
        card = self.deck.take_bottom_card()
        self.assertEqual('Yellow', card.colour)

        next_card = self.deck.take_bottom_card()
        self.assertEqual('Moscow', next_card.name)

    def test_add_card(self):
        new_card = Card('Cherepovets', 'Black')
        self.deck.add_card(new_card)

        self.assertEqual('Cherepovets', self.deck.cards[-1].name)

    def test_add_discard(self):
        discarded_card = Card('Cherepovets', 'Black')
        self.deck.add_discard(discarded_card)

        self.assertEqual('Cherepovets', self.deck.discard[-1].name)

    def test_shuffle(self):
        random.seed(42)
        random.shuffle(self.test_cards)

        random.seed(42)
        self.deck.shuffle()
        self.assertEqual(self.test_cards, self.deck.cards)


TEST_CITIES = [
    City('London', 'Blue'),         City('Oxford', 'Blue'),
    City('Cambridge', 'Blue'),      City('Brighton', 'Blue'),
    City('Southampton', 'Blue'),    City('Bristol', 'Blue'),
    City('Plymouth', 'Blue'),       City('Liverpool', 'Blue'),
    City('Manchester', 'Blue'),     City('Leeds', 'Blue'),
    City('Washington', 'Yellow'),   City('Detroit', 'Yellow'),
    City('New', 'York'),            City('Indianapolis', 'Yellow'),
    City('Chicago', 'Yellow'),      City('Nashville', 'Yellow'),
    City('Atlanta', 'Yellow'),      City('Charlotte', 'Yellow'),
    City('Jacksonville', 'Yellow'), City('Bejing', 'Red'),
    City('Tianjin', 'Red'),         City('Baoding', 'Red'),
    City('Jinan', 'Red'),           City('Jining', 'Red'),
    City('Weifang', 'Red'),         City('Linyi', 'Red'),
    City('Qingdao', 'Red'),         City('Yantai', 'Red'),
    City('Shijiazhuang', 'Red'),    City('Moscow', 'Black'),
    City('Tver', 'Black'),          City('Kaluga', 'Black'),
    City('Tula', 'Black'),          City('Cherepovets', 'Black'),
    City('Vologda', 'Black'),       City('Bryansk', 'Black'),
    City('Smolensk', 'Black'),      City('Oryol', 'Black'),
    City('Krusk', 'Black'),         City('Belgorod', 'Black'),
]


class PlayerDeckTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cities = TEST_CITIES

    def setUp(self):
        self.deck = PlayerDeck()

    def test_prepare(self):
        self.deck.prepare(self.cities)

        self.assertIsInstance(self.deck.cards[10], PlayerCard)
        self.assertEqual('London', self.deck.cards[0].name)
        self.assertEqual('Black', self.deck.cards[29].colour)

    def test_multiple_prepare(self):
        self.deck.prepare(self.cities)
        deck_size = len(self.deck.cards)

        self.deck.prepare(self.cities)
        self.assertEqual(deck_size, len(self.deck.cards))

    def test_add_epidemics(self):
        self.deck.prepare(self.cities)

        random.seed(42)
        self.deck.add_epidemics(6)

        self.assertEqual(46, len(self.deck.cards))
        self.assertEqual('Epidemic', self.deck.cards[13].name)
        self.assertEqual('Epidemic', self.deck.cards[24].name)
        self.assertEqual('London', self.deck.cards[33].name)


class InfectDeckTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cities = TEST_CITIES

    def setUp(self):
        self.deck = InfectDeck()

    def test_prepare(self):
        self.deck.prepare(self.cities)

        self.assertIsInstance(self.deck.cards[10], InfectCard)
        self.assertEqual('London', self.deck.cards[0].name)
        self.assertEqual('Black', self.deck.cards[29].colour)

    def test_multiple_prepare(self):
        self.deck.prepare(self.cities)
        deck_size = len(self.deck.cards)

        self.deck.prepare(self.cities)
        self.assertEqual(deck_size, len(self.deck.cards))

    def test_shuffle_discard_to_top(self):
        self.deck.prepare(self.cities)
        for i in range(10):
            self.deck.add_discard(self.deck.take_top_card())

        random.seed(42)
        self.deck.shuffle_discard_to_top()

        self.assertFalse(self.deck.discard)
        self.assertEqual('London', self.deck.cards[8].name)
        self.assertEqual('Washington', self.deck.cards[10].name)

