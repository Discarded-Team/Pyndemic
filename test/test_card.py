from unittest import TestCase

from pyndemic.card import Card
from pyndemic.game import Game
from .test_helpers import MockController


class CardTestCase(TestCase):
    def setUp(self):
        self.controller = MockController()
        self._ctx = self.controller._ctx

        self.pg = Game()
        self.pg.settings = self.controller.settings
        self.controller.game = self.pg

    def test_init(self):
        card = Card('London', 'Blue')
        self.assertEqual('London', card.name)
        self.assertEqual('Blue', card.colour)
