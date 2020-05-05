# coding: utf-8
import unittest
from unittest import TestCase, skip, expectedFailure

import os.path as op
import random

from src import config
from src.exceptions import *
from src.game import Game
from src.city import City
from src.disease import Disease
from src.card import Card, PlayerCard, InfectCard
from src.deck import Deck, PlayerDeck, InfectDeck
from src.player import Player


SETTINGS_LOCATION = op.join(op.dirname(__file__), 'test_settings.cfg')


class GameSetupTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.settings = config.get_settings(SETTINGS_LOCATION, refresh=True)

    def setUp(self):
        self.pg = Game()
        self.pg.settings = self.settings

    def test_add_player(self):
        players = [Player('Evie'), Player('Amelia')]

        for player in players:
            self.pg.add_player(player)

            with self.subTest(player=player):
                self.assertIs(self.pg, player.game)
                self.assertIn(player, self.pg.players)
                self.assertEqual(player.name, self.pg.players[-1].name)

    def test_get_infection_rate(self):
        self.pg.get_infection_rate()
        self.assertEqual(2, self.pg.infection_rate)

    def test_get_new_cities(self):
        self.pg.get_new_cities()

        self.assertEqual(40, len(self.pg.city_map))
        self.assertIn('London', self.pg.city_map)

        city = self.pg.city_map['London']
        self.assertEqual('London', city.name)
        self.assertEqual('Blue', city.colour)
        self.assertEqual('Yellow', self.pg.city_map['Washington'].colour)

        self.assertEqual(6, len(city.connected_cities))
        self.assertIn(self.pg.city_map['Washington'], city.connected_cities)
        self.assertNotIn(self.pg.city_map['Liverpool'], city.connected_cities)

    def test_make_cities(self):
        # TODO: get around implicit method call
        self.pg.get_new_cities()
        city = self.pg.city_map['London']

        self.assertEqual(6, len(city.connected_cities))
        self.assertIn(self.pg.city_map['Washington'], city.connected_cities)
        self.assertNotIn(self.pg.city_map['Liverpool'], city.connected_cities)

    def test_get_new_decks(self):
        self.pg.get_new_cities()
        self.pg.get_new_decks()

        deck = self.pg.player_deck
        self.assertEqual('London', deck.cards[0].name)
        self.assertEqual('Black', deck.cards[29].colour)

        deck = self.pg.infect_deck
        self.assertEqual('London', deck.cards[0].name)
        self.assertEqual('Black', deck.cards[29].colour)

    def test_get_new_diseases(self):
        self.pg.get_new_diseases()

        self.assertEqual('Red', self.pg.diseases['Red'].colour)
        self.assertEqual(30, self.pg.diseases['Blue'].public_health)

    def test_set_starting_epidemics(self):
        self.pg.set_starting_epidemics()
        self.assertEqual(4, self.pg.starting_epidemics)

    def test_setup_game(self):
        del self.pg.settings

        players = [Player('Evie'), Player('Amelia')]
        for player in players:
            self.pg.add_player(player)

        self.pg.setup_game(SETTINGS_LOCATION)

        self.assertEqual(self.pg.settings, self.settings)

        self.assertEqual(0, self.pg.epidemic_count)
        self.assertEqual(0, self.pg.outbreak_count)
        self.assertFalse(self.pg.game_won)
        self.assertFalse(self.pg.game_over)

        self.assertEqual(2, self.pg.infection_rate)

        self.assertIn('New York', self.pg.city_map)
        self.newyork = self.pg.city_map['New York']
        self.assertEqual('New York', self.newyork.name)
        self.assertEqual('Yellow', self.newyork.colour)
        self.assertEqual(3, len(self.newyork.connected_cities))
        for colour in ('Blue', 'Red', 'Yellow', 'Black'):
            self.assertIn(colour, self.newyork.infection_levels)

        top_player_card = self.pg.player_deck.take_top_card()
        top_infect_card = self.pg.infect_deck.take_top_card()
        self.assertEqual('London', top_player_card.name)
        self.assertEqual('London', top_infect_card.name)

        self.assertEqual('Red', self.pg.diseases['Red'].colour)
        self.assertEqual(30, self.pg.diseases['Black'].public_health)

        self.assertEqual(4, self.pg.starting_epidemics)


class GameTestCase(unittest.TestCase):
    def setUp(self):
        random.seed(42)
        self.player1 = Player('Evie')
        self.player2 = Player('Amelia')
        self.pg = Game()
        self.pg.add_player(self.player1)
        self.pg.add_player(self.player2)
        self.pg.setup_game(SETTINGS_LOCATION)

    def test_all_one_colour(self):
        card_names = ['London', 'Oxford', 'Cambridge', 'Brighton', 'Southampton']
        self.assertTrue(self.pg.all_one_colour(card_names))

        card_names[3] = 'Moscow'
        self.assertFalse(self.pg.all_one_colour(card_names))

    def test_all_diseases_cured(self):
        self.assertFalse(self.pg.all_diseases_cured())

        self.pg.diseases['Yellow'].cured = True
        self.assertFalse(self.pg.all_diseases_cured())

        self.pg.diseases['Blue'].cured = True
        self.pg.diseases['Black'].cured = True
        self.assertFalse(self.pg.all_diseases_cured())

        self.pg.diseases['Red'].cured = True
        self.assertTrue(self.pg.all_diseases_cured())

    def test_add_epidemics(self):
        self.pg.add_epidemics()
        num_epidemics = len({card for card in self.pg.player_deck.cards
                             if card.name == 'Epidemic'})
        self.assertTrue(self.pg.starting_epidemics, num_epidemics)

    def test_infect_city(self):
        self.pg.infect_city('London', 'Blue')
        self.assertEqual(1, self.pg.city_map['London'].infection_levels['Blue'])

        self.pg.diseases['Blue'].public_health = 0
        with self.assertRaises(GameCrisisException):
            self.pg.infect_city('London', 'Blue')

    def test_infect_city_phase(self):
        self.pg.infect_city_phase()
        self.assertEqual(1, self.pg.city_map['London'].infection_levels['Blue'])
        self.assertEqual(1, self.pg.city_map['Oxford'].infection_levels['Blue'])
        self.assertEqual(2, len(self.pg.infect_deck.discard))
        self.assertEqual('London', self.pg.infect_deck.discard[0].name)
        self.assertEqual(28, self.pg.diseases['Blue'].public_health)

    def test_epidemic_phase(self):
        self.pg.epidemic_phase()
        self.assertEqual(3, self.pg.city_map['Belgorod'].infection_levels['Black'])
        top_infect_card = self.pg.infect_deck.take_top_card()
        self.assertEqual('Belgorod', top_infect_card.name)
        self.assertEqual('Black', top_infect_card.colour)
        self.assertEqual(1, self.pg.epidemic_count)
        self.assertEqual(0, len(self.pg.infect_deck.discard))

    def test_outbreak_trigger(self):
        for i in range(4):
            self.pg.infect_city('London', 'Blue')
        self.assertEqual(3, self.pg.city_map['London'].infection_levels['Blue'])
        self.assertEqual(1, self.pg.city_map['Oxford'].infection_levels['Blue'])
        self.assertEqual(1, self.pg.city_map['Cambridge'].infection_levels['Blue'])
        self.assertEqual(1, self.pg.city_map['Brighton'].infection_levels['Blue'])
        self.assertEqual(1, self.pg.city_map['Washington'].infection_levels['Blue'])
        self.assertEqual(1, self.pg.city_map['Bejing'].infection_levels['Blue'])
        self.assertEqual(1, self.pg.city_map['Moscow'].infection_levels['Blue'])
        self.assertEqual(1, self.pg.outbreak_count)

    def test_outbreak(self):
        self.pg.outbreak('London', 'Blue')
        self.assertEqual(1, self.pg.city_map['Oxford'].infection_levels['Blue'])
        self.assertEqual(1, self.pg.city_map['Cambridge'].infection_levels['Blue'])
        self.assertEqual(1, self.pg.city_map['Brighton'].infection_levels['Blue'])
        self.assertEqual(1, self.pg.city_map['Washington'].infection_levels['Blue'])
        self.assertEqual(1, self.pg.city_map['Bejing'].infection_levels['Blue'])
        self.assertEqual(1, self.pg.city_map['Moscow'].infection_levels['Blue'])

        self.pg.outbreak_count = 7
        self.pg.outbreak_stack.clear()
        with self.assertRaises(GameCrisisException):
            self.pg.outbreak('London', 'Blue')

    def test_shuffle(self):
        self.assertEqual('London', self.pg.player_deck.take_top_card().name)
        self.pg.player_deck.shuffle()
        self.assertNotEqual('Oxford', self.pg.player_deck.take_top_card().name)

        self.assertEqual('London', self.pg.infect_deck.take_top_card().name)
        self.pg.infect_deck.shuffle()
        self.assertNotEqual('Oxford', self.pg.infect_deck.take_top_card().name)

    def test_start_game(self):
        self.pg.start_game()
        self.top_player_card = self.pg.player_deck.take_top_card()
        self.top_infect_card = self.pg.infect_deck.take_top_card()
        self.assertEqual(9, len(self.pg.infect_deck.discard))
        self.assertEqual(0, len(self.pg.player_deck.discard))
        self.assertEqual(3, self.pg.city_map['Brighton'].infection_levels['Blue'])
        self.assertEqual(1, self.pg.city_map['Detroit'].infection_levels['Yellow'])
        self.assertEqual(2, self.pg.city_map['Smolensk'].infection_levels['Black'])
        self.assertEqual(4, len(self.player1.hand))
        self.assertEqual(4, len(self.player2.hand))
        self.assertNotEqual('London', self.top_player_card.name)
        self.assertNotEqual('London', self.top_infect_card.name)
        self.assertEqual('London', self.pg.players[0].location.name)
        self.assertEqual('London', self.pg.players[1].location.name)
        self.assertTrue(self.pg.city_map['London'].has_lab)

        for i in range (10):
            self.pg.draw_card(self.player1)
        self.assertEqual(1, self.pg.epidemic_count)

    def test_initial_infect_phase(self):
        self.pg.inital_infect_phase()
        self.assertEqual(3, self.pg.city_map['London'].infection_levels['Blue'])
        self.assertEqual(3, self.pg.city_map['Oxford'].infection_levels['Blue'])
        self.assertEqual(3, self.pg.city_map['Cambridge'].infection_levels['Blue'])
        self.assertEqual(2, self.pg.city_map['Brighton'].infection_levels['Blue'])
        self.assertEqual(2, self.pg.city_map['Southampton'].infection_levels['Blue'])
        self.assertEqual(2, self.pg.city_map['Bristol'].infection_levels['Blue'])
        self.assertEqual(1, self.pg.city_map['Plymouth'].infection_levels['Blue'])
        self.assertEqual(1, self.pg.city_map['Liverpool'].infection_levels['Blue'])
        self.assertEqual(1, self.pg.city_map['Manchester'].infection_levels['Blue'])
        self.assertEqual(9, len(self.pg.infect_deck.discard))
        self.assertEqual(12, self.pg.diseases['Blue'].public_health)

    def test_draw_initial_hands(self):
        test_cards = self.pg.player_deck.cards[:8]
        self.pg.draw_initial_hands()

        for i, player in enumerate(self.pg.players):
            with self.subTest(i=i, player=player):
                self.assertEqual(4, len(player.hand))
                self.assertEqual(test_cards[i * 4 + 3].name, player.hand[3].name)

    def test_draw_card(self):
        self.pg.draw_card(self.player1)
        self.assertEqual('London', self.player1.hand[0].name)

        self.pg.player_deck.cards = []
        with self.assertRaises(GameCrisisException):
            self.pg.draw_card(self.player1)

    def test_get_new_diseaes(self):
        self.assertFalse(self.pg.diseases['Blue'].cured)
        self.assertFalse(self.pg.diseases['Red'].cured)
        self.pg.diseases['Blue'].cured = True
        self.assertTrue(self.pg.diseases['Blue'].cured)


if __name__ == '__main__':
    unittest.main()
