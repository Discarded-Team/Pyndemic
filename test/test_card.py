from unittest import TestCase

from pyndemic.card import Card


class CardTestCase(TestCase):
    def test_init(self):
        card = Card('London', 'Blue')
        self.assertEqual('London', card.name)
        self.assertEqual('Blue', card.colour)
