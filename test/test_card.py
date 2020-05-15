# coding: utf-8

from unittest import TestCase, skip, expectedFailure

from pyndemic.card import Card # , CharacterCard, InfectCard


class CardTestCase(TestCase):
    def test_init(self):
        card = Card('London', 'Blue')
        self.assertEqual('London', card.name)
        self.assertEqual('Blue', card.colour)
