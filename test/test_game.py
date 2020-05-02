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
        self.assertEqual(30, self.pg.diseases['Blue'].cubes_at_bank)

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

        self.assertIn('Yellow', City.cube_colours)
        City.cube_colours = []

        self.assertEqual(2, self.pg.infection_rate)

        self.assertIn('New York', self.pg.city_map)
        self.newyork = self.pg.city_map['New York']
        self.assertEqual('New York', self.newyork.name)
        self.assertEqual('Yellow', self.newyork.colour)
        self.assertEqual(3, len(self.newyork.connected_cities))

        top_player_card = self.pg.player_deck.take_top_card()
        top_infect_card = self.pg.infect_deck.take_top_card()
        self.assertEqual('London', top_player_card.name)
        self.assertEqual('London', top_infect_card.name)

        self.assertEqual('Red', self.pg.diseases['Red'].colour)
        self.assertEqual(30, self.pg.diseases['Black'].cubes_at_bank)

        self.assertEqual(4, self.pg.starting_epidemics)


class GameTestCase(unittest.TestCase):
    def setUp(self):
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
        self.assertFalse(self.pg.has_x_cube_city(3))
        for i in range(0,11):
            self.pg.draw_card(self.player1)
        self.assertEqual(1, self.pg.epidemic_count)
        self.assertTrue(self.pg.has_x_cube_city(3))

    def test_infect_city(self):
        self.pg.infect_city('London', 'Blue')
        self.assertEqual(1, self.pg.city_map['London'].cubes['Blue'])

        self.pg.diseases['Blue'].cubes_at_bank = 0
        with self.assertRaises(GameCrisisException):
            self.pg.infect_city('London', 'Blue')

    def test_infect_city_phase(self):
        self.pg.infect_city_phase()
        self.assertEqual(1, self.pg.city_map['London'].cubes['Blue'])
        self.assertEqual(1, self.pg.city_map['Oxford'].cubes['Blue'])
        self.assertEqual(2, len(self.pg.infect_deck.discard))
        self.assertEqual('London', self.pg.infect_deck.discard[0].name)
        self.assertEqual(28, self.pg.diseases['Blue'].cubes_at_bank)

    def test_epidemic_phase(self):
        self.pg.epidemic_phase()
        self.assertEqual(3, self.pg.city_map['Belgorod'].cubes['Black'])
        top_infect_card = self.pg.infect_deck.take_top_card()
        self.assertEqual('Belgorod', top_infect_card.name)
        self.assertEqual('Black', top_infect_card.colour)
        self.assertEqual(1, self.pg.epidemic_count)
        self.assertEqual(0, len(self.pg.infect_deck.discard))

    def test_outbreak_trigger(self):
        for i in range(4):
            self.pg.infect_city('London', 'Blue')
        self.assertEqual(3, self.pg.city_map['London'].cubes['Blue'])
        self.assertEqual(1, self.pg.city_map['Oxford'].cubes['Blue'])
        self.assertEqual(1, self.pg.city_map['Cambridge'].cubes['Blue'])
        self.assertEqual(1, self.pg.city_map['Brighton'].cubes['Blue'])
        self.assertEqual(1, self.pg.city_map['Washington'].cubes['Blue'])
        self.assertEqual(1, self.pg.city_map['Bejing'].cubes['Blue'])
        self.assertEqual(1, self.pg.city_map['Moscow'].cubes['Blue'])
        self.assertEqual(1, self.pg.outbreak_count)

    def test_outbreak(self):
        self.pg.outbreak('London', 'Blue')
        self.assertEqual(1, self.pg.city_map['Oxford'].cubes['Blue'])
        self.assertEqual(1, self.pg.city_map['Cambridge'].cubes['Blue'])
        self.assertEqual(1, self.pg.city_map['Brighton'].cubes['Blue'])
        self.assertEqual(1, self.pg.city_map['Washington'].cubes['Blue'])
        self.assertEqual(1, self.pg.city_map['Bejing'].cubes['Blue'])
        self.assertEqual(1, self.pg.city_map['Moscow'].cubes['Blue'])

        self.pg.outbreak_count = 7
        self.pg.outbreak_stack.clear()
        with self.assertRaises(GameCrisisException):
            self.pg.outbreak('London', 'Blue')

    def test_shuffle(self):
        import random
        random.seed(42)

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
        self.assertTrue(self.pg.has_x_cube_city(3))
        self.assertEqual(3, self.pg.get_count_x_cube_city(3))
        self.assertTrue(self.pg.has_x_cube_city(2))
        self.assertEqual(3, self.pg.get_count_x_cube_city(2))
        self.assertTrue(self.pg.has_x_cube_city(1))
        self.assertEqual(3, self.pg.get_count_x_cube_city(1))
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
        self.assertEqual(3, self.pg.city_map['London'].cubes['Blue'])
        self.assertEqual(3, self.pg.city_map['Oxford'].cubes['Blue'])
        self.assertEqual(3, self.pg.city_map['Cambridge'].cubes['Blue'])
        self.assertEqual(2, self.pg.city_map['Brighton'].cubes['Blue'])
        self.assertEqual(2, self.pg.city_map['Southampton'].cubes['Blue'])
        self.assertEqual(2, self.pg.city_map['Bristol'].cubes['Blue'])
        self.assertEqual(1, self.pg.city_map['Plymouth'].cubes['Blue'])
        self.assertEqual(1, self.pg.city_map['Liverpool'].cubes['Blue'])
        self.assertEqual(1, self.pg.city_map['Manchester'].cubes['Blue'])
        self.assertEqual(9, len(self.pg.infect_deck.discard))
        self.assertEqual(12, self.pg.diseases['Blue'].cubes_at_bank)

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

    def test_reset_distances(self):
        self.pg.reset_distances()
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.pg.draw_card(self.player1)
        self.assertTrue(self.player1.build_lab())
        self.assertEqual(999, self.pg.city_map['London'].distance)
        self.assertEqual(999, self.pg.city_map['Moscow'].distance)
        self.pg.set_lab_distances()
        self.assertNotEqual(999, self.pg.city_map['London'].distance)
        self.assertNotEqual(999, self.pg.city_map['Moscow'].distance)
        self.pg.reset_distances()
        self.assertEqual(999, self.pg.city_map['London'].distance)
        self.assertEqual(999, self.pg.city_map['Moscow'].distance)

    def test_set_city_distance_name(self):
        self.pg.set_city_distance_name('Leeds')
        self.assertEqual(2, self.pg.city_map['London'].distance)
        self.assertEqual(3, self.pg.city_map['Moscow'].distance)

    def test_set_cities_distances_names(self):
        cities = ['Leeds', 'Atlanta', 'Moscow']
        self.pg.set_cities_distances_names(cities)
        self.assertEqual(1, self.pg.city_map['London'].distance)
        self.assertEqual(0, self.pg.city_map['Moscow'].distance)

    def test_set_lab_distances(self):
        for i in range(21):
            self.pg.draw_card(self.player1)
        self.player1.set_location('London')
        self.pg.start_turn(self.player1)
        self.assertTrue(self.player1.build_lab())
        self.player1.set_location('New York')
        self.pg.draw_card(self.player1)
        self.assertTrue(self.player1.build_lab())
        self.player1.set_location('Jinan')
        self.pg.set_lab_distances()
        self.assertEqual(0, self.pg.city_map['London'].distance)
        self.assertEqual(1, self.pg.city_map['Moscow'].distance)
        self.assertEqual(3, self.player1.get_distance_from_lab())


if __name__ == '__main__':
    unittest.main()
