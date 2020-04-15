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


SETTINGS_LOCATION = op.join(op.dirname(__file__), 'test_settings.cfg')


class AIControllerTestCase(TestCase):
    def setUp(self):
        self.player = Player('Evie')
        AIController.number_AI = 0

    def tearDown(self):
        AIController.number_AI = 0

    def test_init(self):
        controller = AIController(self.player)
        self.assertEqual(1, AIController.number_AI)
        self.assertIs(self.player, controller.player)
        self.assertEqual('AIController1', controller.name)


    @skip('\'PandemicGame.all_one_colour\' method is not provided yet.')
    def test_cure_possible(self):
        city = City('London', 'Blue')
        city.has_lab = True
        self.player.hand = [PlayerCard('City' + s, 'Blue') for s in '12345']
        self.player.location = city
        self.player.action_count = 4

        controller = AIController(self.player)
        self.assertTrue(controller.cure_possible())

        city.has_lab = False
        self.assertFalse(controller.cure_possible())

        city.has_lab = True
        self.player.hand[3] = PlayerCard('RedCity', 'Red')
        self.assertFalse(controller.cure_possible())


    def test_build_lab_sensible(self):
        game = PandemicGame()
        game.add_player(self.player)
        game.setup_game(SETTINGS_LOCATION)

        self.player.action_count = 4
        for i in range(21):
            game.draw_card(self.player)

        game.city_map['London'].has_lab = True
        controller = self.player.controller
        self.player.set_location('London')
        self.assertFalse(controller.build_lab_sensible())

        self.player.set_location('Jacksonville')
        self.assertTrue(controller.build_lab_sensible())

        self.player.set_location('Oxford')
        self.assertFalse(controller.build_lab_sensible())

