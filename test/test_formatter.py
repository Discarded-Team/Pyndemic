import unittest

import os.path as op
import random

from src import config
from src.game import Game
from src.city import City
from src.disease import Disease
from src.card import Card, PlayerCard, InfectCard
from src.deck import Deck, PlayerDeck, InfectDeck
from src.player import Player
from src.formatter import BaseFormatter


SETTINGS_LOCATION = op.join(op.dirname(__file__), 'test_settings.cfg')


class GameStateSerialisationCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.settings = config.get_settings(SETTINGS_LOCATION, refresh=True)

    def setUp(self):
        random.seed(42)
        self.player1 = Player('Evie')
        self.player2 = Player('Amelia')
        self.pg = Game()
        self.pg.add_player(self.player1)
        self.pg.add_player(self.player2)
        self.pg.setup_game(SETTINGS_LOCATION)
        self.pg.start_game()

        top_player_card = self.pg.player_deck.take_top_card()
        top_infect_card = self.pg.infect_deck.take_top_card()
        self.pg.player_deck.discard.append(top_player_card)
        self.pg.infect_deck.discard.append(top_infect_card)

    def test_game_to_dict(self):
        output = BaseFormatter.game_to_dict(self.pg)
        self.assertEqual(2, len(output['players']))
        self.assertEqual('Evie', output['players'][0]['name'])
        self.assertEqual('Amelia', output['players'][1]['name'])
        # other subdicts are tested for player_to_dict()

        self.assertEqual(1, len(output['player_deck_discard']))
        self.assertEqual(10, len(output['infect_deck_discard'])) # 9 start + 1
        self.assertEqual('Plymouth', output['player_deck_discard'][0]['name'])
        self.assertEqual('Tula', output['infect_deck_discard'][9]['name'])

        self.assertEqual(4, len(output['diseases']))
        self.assertEqual('Blue', output['diseases']['Blue']['colour'])
        # other subdicts are tested for disease_to_dict()

        self.assertEqual(40, len(output['cities']))
        self.assertTrue(output['cities']['London']['has_lab'])
        self.assertFalse(output['cities']['Moscow']['has_lab'])
        self.assertEqual('London', output['cities']['London']['name'])
        # other subdicts are tested for city_to_dict()

        self.assertEqual(2, output['infection_rate'])
        self.assertEqual(0, output['epidemic_count'])


class CardSerialisationTestCase(unittest.TestCase):
    def setUp(self):
        self.card = Card('London', 'Blue')

    def test_card_to_dict(self):
        output = BaseFormatter.card_to_dict(self.card)
        self.assertEqual('London', output['name'])
        self.assertEqual('Blue', output['colour'])


class DeckSerialisationTestCase(unittest.TestCase):
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

    def test_deck_to_dict(self):
        self.deck.clear()
        self.assertEqual([], BaseFormatter.deck_to_list(self.deck))

        discarded_card = Card('Cherepovets', 'Black')
        self.deck.add_discard(discarded_card)
        discarded_card = Card('London', 'Blue')
        self.deck.add_discard(discarded_card)
        output = BaseFormatter.deck_to_list(self.deck)
        self.assertEqual('Cherepovets', output[0]['name'])
        self.assertEqual('Black', output[0]['colour'])
        self.assertEqual('London', output[1]['name'])


class CitySerialisationTestCase(unittest.TestCase):
    def setUp(self):
        self.city = City('London', 'Blue')
        self.city.infection_levels['Black'] = 2
        self.city.infection_levels['Blue'] = 3

    def test_city_to_dict(self):
        output = BaseFormatter.city_to_dict(self.city)
        self.assertEqual('London', output['name'])
        self.assertFalse(output['has_lab'])
        self.assertEqual('Blue', output['colour'])
        self.assertEqual(2, output['infection_levels']['Black'])
        self.assertEqual(3, output['infection_levels']['Blue'])


class DiseaseSerialisationTestCase(unittest.TestCase):
    def setUp(self):
        self.disease = Disease('Blue', 42)

    def test_disease_to_dict(self):
        output = BaseFormatter.disease_to_dict(self.disease)
        self.assertEqual('Blue', output['colour'])
        self.assertEqual(42, output['public_health'])
        self.assertFalse(output['cured'])


class PlayerSerialisationTestCase(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.game = Game()
        self.player = Player('Alice')
        self.game.add_player(self.player)
        self.game.setup_game(SETTINGS_LOCATION)
        self.player.set_location('London')
        self.player.action_count = 4
        self.player.hand = [PlayerCard('London', 'Blue'),
                            PlayerCard('New York', 'Yellow')]

    def test_player_to_dict(self):
        output = BaseFormatter.player_to_dict(self.player)
        self.assertEqual('Alice', output['name'])
        self.assertEqual(4, output['action_count'])
        self.assertEqual(2, len(output['hand']))
        self.assertEqual('London', output['hand'][0]['name'])
        self.assertEqual('London', output['location'])


if __name__ == '__main__':
    unittest.main()
