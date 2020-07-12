from unittest import TestCase
from unittest.mock import patch

from pyndemic.card import (Card, PlayerCard, CityCard, EpidemicCard,
                           ActionCard, InfectCard)
from pyndemic.character import Character
from .test_helpers import construct_mock_context


class CardTestCase(TestCase):
    def test_init(self):
        card = Card('London', 'Blue')
        self.assertEqual('London', card.name)
        self.assertEqual('Blue', card.colour)


class PlayerCardTestCase(TestCase):
    def setUp(self):
        self.character = Character('Bob')

    def test_on_draw(self):
        card = PlayerCard('London', 'Blue')
        card.on_draw(self.character)
        self.assertIn(card, self.character.hand)


class CityCardTestCase(TestCase):
    pass


class EpidemicCardTestCase(TestCase):
    def setUp(self):
        self._ctx = construct_mock_context()
        self.mock_game = self._ctx['controller']().game

    def test_init(self):
        card = EpidemicCard()
        self.assertEqual('Epidemic', card.name)
        self.assertIsNone(card.colour)

    def test_on_draw(self):
        card = EpidemicCard()
        card.on_draw('Fake character')

        self.mock_game.epidemic_phase.assert_called()


class ActionCardTestCase(TestCase):
    def test_init(self):
        card = ActionCard()
        self.assertIsNone(card.name)
        self.assertIsNone(card.colour)


class InfectCardTestCase(TestCase):
    def setUp(self):
        self._ctx = construct_mock_context()
        self.mock_game = self._ctx['controller']().game

    @patch.object(InfectCard, 'on_play')
    def test_on_draw(self, mock_method):
        card = InfectCard('London', 'Blue')
        card.on_draw('Fake character')

        mock_method.assert_called_with('Fake character')

    def test_on_play(self):
        card = InfectCard('London', 'Blue')
        card.on_play('Fake character')

        self.mock_game.infect_city.assert_called_with(card.name, card.colour)
        self.mock_game.outbreak_stack.clear.assert_called()
        self.mock_game.infect_deck.add_discard.assert_called_with(card)
