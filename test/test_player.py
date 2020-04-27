# coding: utf-8
import unittest
from unittest import TestCase, skip, expectedFailure

import os.path as op
import random

import config
from exceptions import *
from game import Game
from city import City
from disease import Disease
from card import Card, PlayerCard, InfectCard
from deck import Deck, PlayerDeck, InfectDeck
from player import Player


SETTINGS_LOCATION = op.join(op.dirname(__file__), 'test_settings.cfg')


class PlayerTestCase(TestCase):
    def setUp(self):
        self.game = Game()
        self.player = Player('Alice')
        self.other_player = Player('Bob')
        self.game.add_player(self.player)
        self.game.add_player(self.other_player)
        self.game.setup_game(SETTINGS_LOCATION)

    def test_init(self):
        player = Player('Bob')
        self.assertEqual('Bob', player.name)
        self.assertIsNone(player.location)
        self.assertEqual([], player.hand)
        self.assertEqual(0, player.action_count)

    def test_get_distance_from_lab(self):
        city_with_lab = self.game.city_map['Plymouth']
        city_with_lab.has_lab = True
        self.player.location = self.game.city_map['London']
        distance = self.player.get_distance_from_lab()
        self.assertEqual(3, distance)

    def test_get_card(self):
        self.player.hand = [PlayerCard('London', 'Blue'),
                            PlayerCard('New York', 'Yellow')]

        card = self.player.get_card('London')
        self.assertIs(self.player.hand[0], card)

        with self.assertRaises(ValueError):
            card = self.player.get_card('Moscow')

    def test_add_card(self):
        top_player_card = self.game.player_deck.take_top_card()
        self.player.add_card(top_player_card)
        self.assertEqual(1, len(self.player.hand))
        self.assertTrue(self.player.hand_contains('London'))

    def test_hand_contains(self):
        self.player.hand = [PlayerCard('London', 'Blue'),
                            PlayerCard('New York', 'Yellow')]

        self.assertTrue(self.player.hand_contains('New York'))
        self.assertFalse(self.player.hand_contains('Oxford'))

    def test_discard_card(self):
        self.game.draw_card(self.player)
        card = self.player.hand[0]

        success = self.player.discard_card(card.name)
        self.assertTrue(success)
        self.assertIn(card, self.game.player_deck.discard)
        self.assertNotIn(card, self.player.hand)

        self.assertFalse(self.player.discard_card('Moscow'))

    def test_set_location(self):
        city = self.game.city_map['London']
        self.player.set_location('London')
        self.assertIs(city, self.player.location)

    def test_check_charter_flight(self):
        self.player.set_location('London')
        self.assertFalse(self.player.check_charter_flight('London', 'Moscow'))

        self.player.action_count = 1
        self.assertFalse(self.player.check_charter_flight('London', 'Moscow'))

        self.player.hand = [PlayerCard('London', 'Blue'),
                            PlayerCard('Moscow', 'Black')]
        self.assertTrue(self.player.check_charter_flight('London', 'Moscow'))
        self.assertFalse(self.player.check_charter_flight('Moscow', 'London'))

        self.player.action_count = 0
        self.assertFalse(self.player.check_charter_flight('London', 'Moscow'))

        self.player.action_count = 1
        self.player.set_location('Moscow')
        self.assertFalse(self.player.check_charter_flight('London', 'Moscow'))

    def test_charter_flight(self):
        self.player.set_location('London')
        self.player.action_count = 4
        self.game.draw_card(self.player)
        card = self.player.hand[0]

        success = self.player.charter_flight(card.name, 'New York')
        self.assertTrue(success)
        self.assertIn(card, self.game.player_deck.discard)
        self.assertNotIn(card, self.player.hand)
        self.assertEqual('New York', self.player.location.name)
        self.assertEqual(3, self.player.action_count)

        success = self.player.charter_flight('New York', 'Brighton')
        self.assertFalse(success)
        self.assertEqual(1, len(self.game.player_deck.discard))
        self.assertIn(card, self.game.player_deck.discard)
        self.assertEqual(3, self.player.action_count)
        self.assertEqual('New York', self.player.location.name)

    def test_check_direct_flight(self):
        self.player.set_location('London')
        self.player.hand = [PlayerCard('Moscow', 'Black')]
        self.player.action_count = 4

        self.assertFalse(self.player.check_direct_flight('London', 'Bejing'))
        self.assertTrue(self.player.check_direct_flight('London', 'Moscow'))
        self.assertFalse(self.player.check_direct_flight('New York', 'Moscow'))

        self.player.action_count = 0
        self.assertFalse(self.player.check_direct_flight('London', 'Moscow'))

    def test_direct_flight(self):
        self.player.set_location('Moscow')
        self.player.action_count = 4
        self.game.draw_card(self.player)
        card = self.player.hand[0]

        success = self.player.direct_flight('Moscow', card.name)
        self.assertTrue(success)
        self.assertIn(card, self.game.player_deck.discard)
        self.assertNotIn(card, self.player.hand)
        self.assertEqual(card.name, self.player.location.name)
        self.assertEqual(3, self.player.action_count)

        success = self.player.direct_flight('London', 'Brighton')
        self.assertFalse(success)
        self.assertEqual(1, len(self.game.player_deck.discard))
        self.assertIn(card, self.game.player_deck.discard)
        self.assertEqual(3, self.player.action_count)
        self.assertEqual(card.name, self.player.location.name)

    def test_check_cure_disease(self):
        for i in range(9):
            self.game.draw_card(self.player)
        location = self.game.city_map['London']
        self.player.set_location('London')

        card_names = ['Oxford', 'Cambridge', 'Brighton', 'Southampton', 'Bristol']
        self.assertFalse(self.player.check_cure_disease(*card_names))

        location.has_lab = True
        self.assertFalse(self.player.check_cure_disease(*card_names))

        self.player.action_count = 4
        self.assertTrue(self.player.check_cure_disease(*card_names))

        card_names[3] = 'Moscow'
        self.assertFalse(self.player.check_cure_disease(*card_names))

        card_names[3] = 'Oxford'
        self.assertFalse(self.player.check_cure_disease(*card_names))

    def test_cure_disease(self):
        for i in range(9):
            self.game.draw_card(self.player)
        location = self.game.city_map['London']
        self.player.set_location('London')

        self.game.diseases['Blue'].cured = False
        location.has_lab = True
        self.player.action_count = 4
        card_names = ['Cambridge', 'Liverpool', 'Brighton', 'Southampton', 'Manchester']

        success = self.player.cure_disease(*card_names)
        self.assertTrue(success)
        self.assertTrue(self.game.diseases['Blue'].cured)
        self.assertEqual(3, self.player.action_count)
        for card_name in card_names:
            with self.subTest(card_name=card_name):
                self.assertFalse(self.player.hand_contains(card_name))
                self.assertTrue(any(card.name == card_name
                                    for card in self.game.player_deck.discard))

        self.assertFalse(self.player.cure_disease(*card_names))
        self.assertEqual(3, self.player.action_count)

    def test_game_won(self):
        for i in range(9):
            self.game.draw_card(self.player)
        location = self.game.city_map['London']
        self.player.set_location('London')

        self.game.diseases['Blue'].cured = False
        self.game.diseases['Black'].cured = True
        self.game.diseases['Red'].cured = True
        self.game.diseases['Yellow'].cured = True
        location.has_lab = True
        self.player.action_count = 4
        card_names = ['Cambridge', 'Liverpool', 'Brighton', 'Southampton', 'Manchester']

        with self.assertRaises(GameCrisisException):
            success = self.player.cure_disease(*card_names)

    def test_check_share_knowledge(self):
        self.player.hand = [PlayerCard('London', 'Blue'),
                            PlayerCard('Moscow', 'Black')]

        self.player.set_location('London')
        self.other_player.set_location('London')
        self.assertFalse(self.player.check_share_knowledge('London', self.other_player))

        self.player.action_count = 4
        self.assertTrue(self.player.check_share_knowledge('London', self.other_player))
        self.assertFalse(self.player.check_share_knowledge('Moscow', self.other_player))

        self.assertFalse(self.player.check_share_knowledge('London', self.player))

        self.other_player.hand.append(self.player.hand.pop(0))
        self.assertTrue(self.player.check_share_knowledge('London', self.other_player))

        self.other_player.set_location('New York')
        self.assertFalse(self.player.check_share_knowledge('London', self.other_player))

        self.player.set_location('New York')
        self.assertFalse(self.player.check_share_knowledge('New York', self.other_player))

    def test_share_knowledge(self):
        shared_card = PlayerCard('London', 'Blue')
        unshared_card = PlayerCard('Moscow', 'Black')
        self.player.hand = [shared_card, unshared_card]

        self.player.set_location('London')
        self.other_player.set_location('London')
        self.player.action_count = 4

        success = self.player.share_knowledge('London', self.other_player)
        self.assertTrue(success)
        self.assertNotIn(shared_card, self.player.hand)
        self.assertIn(shared_card, self.other_player.hand)
        self.assertEqual(3, self.player.action_count)

        success = self.player.share_knowledge('London', self.other_player)
        self.assertTrue(success)
        self.assertNotIn(shared_card, self.other_player.hand)
        self.assertIn(shared_card, self.player.hand)
        self.assertEqual(2, self.player.action_count)

        success = self.player.share_knowledge('Moskow', self.other_player)
        self.assertFalse(success)
        self.assertNotIn(unshared_card, self.other_player.hand)
        self.assertIn(unshared_card, self.player.hand)
        self.assertEqual(2, self.player.action_count)

    def test_check_treat_disease(self):
        self.game.infect_city('London', 'Blue')
        self.game.infect_city('London', 'Blue')

        self.player.set_location('London')
        self.assertFalse(self.player.check_treat_disease('Blue'))

        self.player.action_count = 4
        self.assertTrue(self.player.check_treat_disease('Blue'))
        self.assertFalse(self.player.check_treat_disease('Red'))

    def test_treat_disease_no_cure(self):
        location = self.game.city_map['London']
        self.player.set_location('London')
        self.player.action_count = 4
        location.cubes['Blue'] = 3
        initial_cubes = self.game.disease_cubes['Blue']

        success = self.player.treat_disease('Blue')
        self.assertTrue(success)
        self.assertEqual(2, location.cubes['Blue'])
        self.assertEqual(initial_cubes + 1, self.game.disease_cubes['Blue'])
        self.assertEqual(3, self.player.action_count)

        initial_cubes = self.game.disease_cubes['Red']
        success = self.player.treat_disease('Red')
        self.assertFalse(success)
        self.assertEqual(2, location.cubes['Blue'])
        self.assertEqual(initial_cubes, self.game.disease_cubes['Red'])
        self.assertEqual(3, self.player.action_count)

        self.player.action_count = 0
        success = self.player.treat_disease('Blue')
        self.assertFalse(success)
        self.assertEqual(2, location.cubes['Blue'])

    def test_treat_disease_cure(self):
        self.game.diseases['Blue'].cured = True
        location = self.game.city_map['London']
        self.player.set_location('London')
        self.player.action_count = 4
        location.cubes['Blue'] = 3

        success = self.player.treat_disease('Blue')
        self.assertTrue(success)
        self.assertEqual(0, location.cubes['Blue'])
        self.assertEqual(3, self.player.action_count)

        location.cubes['Blue'] = 3
        success = self.player.treat_disease('Red')
        self.assertFalse(success)
        self.assertEqual(3, location.cubes['Blue'])
        self.assertEqual(3, self.player.action_count)

        self.player.action_count = 0
        success = self.player.treat_disease('Blue')
        self.assertFalse(success)
        self.assertEqual(3, location.cubes['Blue'])

    def test_check_shuttle_flight(self):
        self.player.set_location('London')
        self.player.action_count = 4

        location = self.game.city_map['London']
        destination = self.game.city_map['Tula']
        location.has_lab = True
        destination.has_lab = True
        self.assertTrue(self.player.check_shuttle_flight('London', 'Tula'))
        self.assertFalse(self.player.check_shuttle_flight('London', 'Tver'))

        destination.has_lab = False
        self.assertFalse(self.player.check_shuttle_flight('London', 'Tula'))

        destination.has_lab = True
        self.player.set_location('New York')
        self.assertFalse(self.player.check_shuttle_flight('London', 'Tula'))

        self.player.set_location('London')
        self.player.action_count = 0
        self.assertFalse(self.player.check_shuttle_flight('London', 'Tula'))

    def test_shuttle_flight(self):
        location = self.game.city_map['London']
        destination = self.game.city_map['Tula']
        location.has_lab = True
        destination.has_lab = True
        self.player.set_location('London')
        self.player.action_count = 4

        success = self.player.shuttle_flight('London', 'Tula')
        self.assertTrue(success)
        self.assertEqual(3, self.player.action_count)
        self.assertEqual('Tula', self.player.location.name)

        success = self.player.shuttle_flight('Tula', 'Moscow')
        self.assertFalse(success)
        self.assertEqual(3, self.player.action_count)
        self.assertEqual('Tula', self.player.location.name)

    def test_check_build_lab(self):
        location = self.game.city_map['London']
        location.has_lab = False

        self.player.set_location('London')
        self.player.action_count = 4

        self.player.hand = [PlayerCard('London', 'Blue'),
                            PlayerCard('Moscow', 'Black')]

        self.assertTrue(self.player.check_build_lab())

        self.player.action_count = 0
        self.assertFalse(self.player.check_build_lab())

        self.player.action_count = 4
        location.has_lab = True
        self.assertFalse(self.player.check_build_lab())

        location.has_lab = False
        self.player.hand = []
        self.assertFalse(self.player.check_build_lab())

    def test_build_lab(self):
        location = self.game.city_map['London']
        location.has_lab = False
        card = PlayerCard('London', 'Blue')
        self.player.hand.append(card)
        self.player.set_location('London')
        self.player.action_count = 4

        success = self.player.build_lab()
        self.assertTrue(success)
        self.assertEqual(3, self.player.action_count)
        self.assertTrue(location.has_lab)
        self.assertNotIn(card, self.player.hand)
        self.assertIn(card, self.game.player_deck.discard)

        location = self.game.city_map['Moscow']
        lab_status = location.has_lab
        card = PlayerCard('Moscow', 'Black')
        self.player.hand.append(card)
        self.player.set_location('Moscow')
        self.player.action_count = 0

        success = self.player.build_lab()
        self.assertFalse(success)
        self.assertIn(card, self.player.hand)
        self.assertNotIn(card, self.game.player_deck.discard)
        self.assertEqual(0, self.player.action_count)
        self.assertEqual(lab_status, location.has_lab)

    def test_check_standard_move(self):
        self.player.set_location('London')
        self.player.action_count = 4

        self.assertTrue(self.player.check_standard_move('London', 'Brighton'))
        self.assertFalse(self.player.check_standard_move('Brighton', 'London'))
        self.assertFalse(self.player.check_standard_move('London', 'Tula'))

        self.player.action_count = 0
        self.assertFalse(self.player.check_standard_move('London', 'Brighton'))


    def standard_move(self, location, destination):
        if self.check_standard_move(location, destination):
            self.set_location(destination)
            self.action_count -= 1
            return True
        return False

    def test_standard_move(self):
        self.player.set_location('London')
        self.player.action_count = 4

        success = self.player.standard_move('London', 'Brighton')
        self.assertTrue(success)
        self.assertEqual(3, self.player.action_count)
        self.assertEqual('Brighton', self.player.location.name)

        success = self.player.standard_move('New York', 'London')
        self.assertFalse(success)
        self.assertEqual(3, self.player.action_count)
        self.assertEqual('Brighton', self.player.location.name)

        success = self.player.standard_move('Brighton', 'New York')
        self.assertFalse(success)
        self.assertEqual(3, self.player.action_count)
        self.assertEqual('Brighton', self.player.location.name)

        self.player.action_count = 0
        success = self.player.standard_move('Brighton', 'London')
        self.assertFalse(success)
        self.assertEqual('Brighton', self.player.location.name)

    def test_check_long_move(self):
        self.player.set_location('London')
        self.player.action_count = 4

        self.assertTrue(self.player.check_long_move('London', 'Plymouth'))
        self.assertTrue(self.player.check_long_move('London', 'Baoding'))
        self.assertFalse(self.player.check_long_move('Baoding', 'London'))

        self.player.set_location('Plymouth')
        self.assertFalse(self.player.check_long_move('Plymouth', 'Baoding'))

    def long_move(self, location, destination):
        if self.check_long_move(location, destination):
            self.action_count -= self.location.distance
            self.set_location(destination)
            return True
        return False

    def test_long_move(self):
        self.player.set_location('London')
        self.player.action_count = 4

        success = self.player.long_move('London', 'Plymouth')
        self.assertTrue(success)
        self.assertEqual(1, self.player.action_count)
        self.assertEqual('Plymouth', self.player.location.name)

        self.player.action_count = 4
        success = self.player.long_move('Plymouth', 'Baoding')
        self.assertFalse(success)
        self.assertEqual(4, self.player.action_count)
        self.assertEqual('Plymouth', self.player.location.name)

