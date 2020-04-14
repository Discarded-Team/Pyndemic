# coding: utf-8
import unittest
from unittest import TestCase, skip, expectedFailure

import os.path as op
import random

import config
from PandemicGame import PandemicGame
from city import City
from disease import Disease
from card import Card, PlayerCard, InfectCard
from deck import Deck, PlayerDeck, InfectDeck
from ai import AIController
from player import Player

# TODO: provide test cases for City and Player classes.


SETTINGS_LOCATION = op.join(op.dirname(__file__), 'test_settings.cfg')


class GameSetupTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.settings = config.get_settings(SETTINGS_LOCATION, refresh=True)

    def setUp(self):
        self.pg = PandemicGame()
        self.pg.settings = self.settings

    def test_add_player(self):
        players = [Player('Evie'), Player('Amelia')]

        for player in players:
            self.pg.add_player(player)

            with self.subTest(player=player):
                self.assertIs(self.pg, player.game)
                self.assertIn(player, self.pg.players)
                self.assertEqual(player.name, self.pg.players[-1].name)
                self.assertEqual(len(self.pg.players), AIController.number_AI)

        AIController.number_AI = 0

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
        self.assertEqual(30, self.pg.disease_cubes['Blue'])

    def test_set_starting_epidemics(self):
        self.pg.set_starting_epidemics()
        self.assertEqual(4, self.pg.starting_epidemics)

    @skip('Fix mistake with AIController setup.')
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
        self.assertEqual(30, self.pg.disease_cubes['Black'])

        self.assertEqual(4, self.pg.starting_epidemics)

        self.assertEqual('London', players[0].location.name)
        self.assertEqual('London', players[1].location.name)

        self.assertEqual(2, AIController.number_AI)


class GameTestCase(unittest.TestCase):
    def setUp(self):
        self.player1 = Player('Evie')
        self.player2 = Player('Amelia')
        self.pg = PandemicGame()
        self.pg.add_player(self.player1)
        self.pg.add_player(self.player2)
        self.pg.setup_game(SETTINGS_LOCATION)

    def test_add_epidemics(self):
        self.pg.add_epidemics()
        self.assertFalse(self.pg.has_x_cube_city(3))
        for i in range(0,11):
            self.pg.draw_card(self.player1)
        self.assertEqual(1, self.pg.epidemic_count)
        self.assertTrue(self.pg.has_x_cube_city(3))

    @skip('Not implemented.')
    def test_complete_round(self):
        self.pg.inital_infect_phase()
        self.pg.draw_inital_hands()
        self.assertEqual(3, self.pg.city_map['Cambridge'].get_cubes('Blue'))
        self.assertEqual(2, self.pg.city_map['Bristol'].get_cubes('Blue'))
        self.pg.complete_round()
        self.assertEqual(0, self.pg.city_map['Cambridge'].get_cubes('Blue'))
        self.assertEqual('Cambridge', self.player1.location.name)
        self.assertEqual(0, self.pg.city_map['Bristol'].get_cubes('Blue'))
        self.assertEqual('Bristol', self.player1.location.name)

    def test_infect_city(self):
        self.pg.infect_city('London', 'Blue')
        self.assertEqual(1, self.pg.city_map['London'].get_cubes('Blue'))

    def test_infect_city_phase(self):
        self.pg.infect_city_phase()
        self.assertEqual(1, self.pg.city_map['London'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Oxford'].get_cubes('Blue'))
        self.assertEqual(2, len(self.pg.infect_deck.discard))
        self.assertEqual('London', self.pg.infect_deck.discard[0].name)
        self.assertEqual(28, self.pg.disease_cubes['Blue'])

    def test_epidemic_phase(self):
        self.pg.epidemic_phase()
        self.assertEqual(3, self.pg.city_map['Belgorod'].get_cubes('Black'))
        top_infect_card = self.pg.infect_deck.take_top_card()
        self.assertEqual('Belgorod', top_infect_card.name)
        self.assertEqual('Black', top_infect_card.colour)
        self.assertEqual(1, self.pg.epidemic_count)
        self.assertEqual(0, len(self.pg.infect_deck.discard))

    def test_outbreak_trigger(self):
        for i in range(4):
            self.pg.infect_city('London', 'Blue')
        self.assertEqual(3, self.pg.city_map['London'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Oxford'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Cambridge'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Brighton'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Washington'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Bejing'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Moscow'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.outbreak_count)

    def test_outbreak(self):
        self.pg.outbreak('London', 'Blue')
        self.assertEqual(1, self.pg.city_map['Oxford'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Cambridge'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Brighton'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Washington'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Bejing'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Moscow'].get_cubes('Blue'))

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
        for i in range (10):
            self.pg.draw_card(self.player1)
        self.assertEqual(1, self.pg.epidemic_count)

    def test_inital_infect_phase(self):
        self.pg.inital_infect_phase()
        self.assertEqual(3, self.pg.city_map['London'].get_cubes('Blue'))
        self.assertEqual(3, self.pg.city_map['Oxford'].get_cubes('Blue'))
        self.assertEqual(3, self.pg.city_map['Cambridge'].get_cubes('Blue'))
        self.assertEqual(2, self.pg.city_map['Brighton'].get_cubes('Blue'))
        self.assertEqual(2, self.pg.city_map['Southampton'].get_cubes('Blue'))
        self.assertEqual(2, self.pg.city_map['Bristol'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Plymouth'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Liverpool'].get_cubes('Blue'))
        self.assertEqual(1, self.pg.city_map['Manchester'].get_cubes('Blue'))
        self.assertEqual(9, len(self.pg.infect_deck.discard))
        self.assertEqual(12, self.pg.disease_cubes['Blue'])

    def test_draw_inital_hands(self):
        test_cards = self.pg.player_deck.cards[:8]
        # TODO: fix typo in method name
        self.pg.draw_inital_hands()

        for i, player in enumerate(self.pg.players):
            with self.subTest(i=i, player=player):
                self.assertEqual(4, len(player.hand))
                self.assertEqual(test_cards[i * 4 + 3].name, player.hand[3].name)

    def test_draw_card(self):
        self.pg.draw_card(self.player1)
        self.assertEqual('London', self.player1.hand[0].name)

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

    @skip('Not implemented.')
    def test_get_inputs(self):
        test_inputs = self.player1.get_inputs()
        self.assertIsNotNone(test_inputs)
        print("check_ing test inputs at start of game")
        print("check_ing first 40 inputs (0-39) for city cubes are all 0")
        for i in range(40):
            self.assertEqual(test_inputs[i],0)
        print("check_ing inputs (40-46 for player1 potential cards are all 0")
        for i in range(40, 46):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs (47-53 for player2 potential cards are all 0")
        for i in range(47, 53):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs (54-60 for player3 potential cards are all 0")
        for i in range(54, 60):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs (61-68 for player4 potential cards are all 0")
        for i in range(61, 68):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs for player cards in discard are all 0")
        for i in range(69, 109):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs for infect cards in discard are all 0")
        for i in range(110, 150):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs for epidemic cards in game is 0")
        self.assertEqual(0, test_inputs[151])
        print("check_ing inputs for epidemic drawn in game is 0")
        self.assertEqual(0, test_inputs[152])
        print("check_ing inputs for outbreaks in game is 0")
        self.assertEqual(0, test_inputs[152])
        print("check_ing inputs for infection rate is 2")
        self.assertEqual(2, test_inputs[152])
        print("check_ing location for each player is set to London")
        self.assertEqual(0.975, test_inputs[153])
        print("check_ing the number of research stations in London is set to 1")
        self.assertEqual(1, test_inputs[158])
        print("check_ing number of research stations in each location is to 0")
        for i in range(159, 199):
            self.assertAlmostEqual(test_inputs[i], 0.975)
        print("checking each disease is set to uncured")
        for i in range(200, 203):
            self.assertEqual(test_inputs[i], 0)
        print("checking the availability of each non movement option (cure disease, treat disease, share knowledge, "
              "buildResaerch) is set to 0")
        for i in range(204, 207):
            self.assertEqual(test_inputs[i], 0)
        print("checking the availability of each movement option (standard, direct, charter, shuttle) is set correctly")
        print("standard possible")
        for i in range(208, 248):
            self.assertEqual(test_inputs[i], 0)
        print("standard not possible")
        for i in range(208, 248):
            self.assertEqual(test_inputs[i], 0)
        print("direct")
        for i in range(249, 289):
            self.assertEqual(test_inputs[i], 0)
        print("charter")
        for i in range(249, 289):
            self.assertEqual(test_inputs[i], 0)
        print("shuttle")
        for i in range(249, 289):
            self.assertEqual(test_inputs[i], 0)
        print("checking available actions for each player is set to 0")
        self.assertEqual(0, test_inputs[300])
        self.assertEqual(0, test_inputs[301])

        self.pg.draw_inital_hands()
        self.pg.inital_infect_phase()
        self.pg.start_turn(self.player1)

        print("check_ing test inputs after game Start during player 1 turn")
        test_inputs = self.player1.get_inputs()
        print("check_ing first 40 inputs (0-39) for city cubes are all correct")
        self.assertEqual(0.25, test_inputs[0])
        self.assertEqual(0.25, test_inputs[3])
        self.assertEqual(0.25, test_inputs[6])
        self.assertEqual(0.50, test_inputs[1])
        self.assertEqual(0.50, test_inputs[4])
        self.assertEqual(0.50, test_inputs[7])
        self.assertEqual(0.75, test_inputs[2])
        self.assertEqual(0.75, test_inputs[5])
        self.assertEqual(0.75, test_inputs[8])
        for i in range(9, 40):
            self.assertEqual(test_inputs[i],0)
        print("check_ing inputs (40-46 for player1 potential cards are all 0")
        self.assertAlmostEqual(0.975, test_inputs[41])
        self.assertAlmostEqual(0.95, test_inputs[42])
        self.assertAlmostEqual(0.925, test_inputs[43])
        self.assertAlmostEqual(0.9, test_inputs[44])
        for i in range(45, 53):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs (47-53 for player2 potential cards are all 0")
        for i in range(47, 53):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs (54-60 for player3 potential cards are all 0")
        for i in range(54, 60):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs (61-68 for player4 potential cards are all 0")
        for i in range(61, 68):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs for player cards in discard are all 0")
        for i in range(69, 109):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs for infect cards in discard are all 0")
        for i in range(110, 150):
            self.assertEqual(test_inputs[i], 0)
        print("check_ing inputs for epidemic cards in game is 0")
        self.assertEqual(0, test_inputs[151])
        print("check_ing inputs for epidemic drawn in game is 0")
        self.assertEqual(0, test_inputs[152])
        print("check_ing inputs for outbreaks in game is 0")
        self.assertEqual(0, test_inputs[152])
        print("check_ing inputs for infection rate is 2")
        self.assertEqual(0, test_inputs[152])
        print("check_ing location for each player is set to London")
        for i in range(153, 158):
            self.assertEqual(test_inputs[i], 0.975)
        print("check_ing number of research stations in each location is to 0.75")
        for i in range(159, 199):
            self.assertEqual(0, test_inputs[i])
        print("checking each disease is set to uncured")
        for i in range(200, 203):
            self.assertEqual(test_inputs[i], 0)
        print("checking the availability of each non movement option (cure disease, treat disease, share knowledge, "
              "buildResaerch) is set to 0")
        for i in range(204, 207):
            self.assertEqual(test_inputs[i], 0)
        print("checking the availability of each movement option (standard, direct, charter, shuttle) is set correctly")
        print("standard possible")
        for i in range(208, 248):
            self.assertEqual(test_inputs[i], 0)
        print("standard not possible")
        for i in range(208, 248):
            self.assertEqual(test_inputs[i], 0)
        print("direct")
        for i in range(249, 289):
            self.assertEqual(test_inputs[i], 0)
        print("charter")
        for i in range(249, 289):
            self.assertEqual(test_inputs[i], 0)
        print("shuttle")
        for i in range(249, 289):
            self.assertEqual(test_inputs[i], 0)
        print("checking available actions for each player is set to 0")
        self.assertEqual(0, test_inputs[300])
        self.assertEqual(0, test_inputs[301])


if __name__ == '__main__':
    unittest.main()
