from unittest import TestCase

import os.path as op
from pyndemic import config
from pyndemic.exceptions import *
from pyndemic.game import Game
from pyndemic.card import PlayerCard
from pyndemic.character import Character


SETTINGS_LOCATION = op.join(op.dirname(__file__), 'test_settings.cfg')


class CharacterTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # without this method the production config is cached
        cls.settings = config.get_settings(SETTINGS_LOCATION, refresh=True)

    def setUp(self):
        self.game = Game()
        self.character = Character('Alice')
        self.other_character = Character('Bob')
        self.game.add_character(self.character)
        self.game.add_character(self.other_character)
        self.game.setup_game(self.settings)

    def test_init(self):
        character = Character('Bob')
        self.assertEqual('Bob', character.name)
        self.assertIsNone(character.location)
        self.assertEqual([], character.hand)
        self.assertEqual(0, character.action_count)

    def test_get_card(self):
        self.character.hand = [PlayerCard('London', 'Blue'),
                               PlayerCard('New York', 'Yellow')]

        card = self.character.get_card('London')
        self.assertIs(self.character.hand[0], card)

        with self.assertRaises(ValueError):
            self.character.get_card('Moscow')

    def test_add_card(self):
        top_player_card = self.game.player_deck.take_top_card()
        self.character.add_card(top_player_card)
        self.assertEqual(1, len(self.character.hand))
        self.assertTrue(self.character.hand_contains('London'))

    def test_hand_contains(self):
        self.character.hand = [PlayerCard('London', 'Blue'),
                               PlayerCard('New York', 'Yellow')]

        self.assertTrue(self.character.hand_contains('New York'))
        self.assertFalse(self.character.hand_contains('Oxford'))

    def test_discard_card(self):
        self.game.draw_card(self.character)
        card = self.character.hand[0]

        success = self.character.discard_card(card.name)
        self.assertTrue(success)
        self.assertIn(card, self.game.player_deck.discard)
        self.assertNotIn(card, self.character.hand)

        self.assertFalse(self.character.discard_card('Moscow'))

    def test_set_location(self):
        city = self.game.city_map['London']
        self.character.set_location('London')
        self.assertIs(city, self.character.location)

    def test_check_charter_flight(self):
        self.character.set_location('London')
        self.assertFalse(self.character.check_charter_flight('London'))

        self.character.action_count = 1
        self.assertFalse(self.character.check_charter_flight('London'))

        self.character.hand = [PlayerCard('London', 'Blue'),
                               PlayerCard('Moscow', 'Black')]
        self.assertTrue(self.character.check_charter_flight('London'))
        self.assertFalse(self.character.check_charter_flight('Moscow'))

        self.character.action_count = 0
        self.assertFalse(self.character.check_charter_flight('London'))

        self.character.action_count = 1
        self.character.set_location('Moscow')
        self.assertFalse(self.character.check_charter_flight('London'))

    def test_charter_flight(self):
        self.character.set_location('London')
        self.character.action_count = 4
        self.game.draw_card(self.character)
        card = self.character.hand[0]

        success = self.character.charter_flight(card.name, 'New York')
        self.assertTrue(success)
        self.assertIn(card, self.game.player_deck.discard)
        self.assertNotIn(card, self.character.hand)
        self.assertEqual('New York', self.character.location.name)
        self.assertEqual(3, self.character.action_count)

        success = self.character.charter_flight('New York', 'Brighton')
        self.assertFalse(success)
        self.assertEqual(1, len(self.game.player_deck.discard))
        self.assertIn(card, self.game.player_deck.discard)
        self.assertEqual(3, self.character.action_count)
        self.assertEqual('New York', self.character.location.name)

    def test_check_direct_flight(self):
        self.character.set_location('London')
        self.character.hand = [PlayerCard('Moscow', 'Black')]
        self.character.action_count = 4

        self.assertFalse(self.character.check_direct_flight('London', 'Bejing'))
        self.assertTrue(self.character.check_direct_flight('London', 'Moscow'))
        self.assertFalse(self.character.check_direct_flight('New York', 'Moscow'))

        self.character.action_count = 0
        self.assertFalse(self.character.check_direct_flight('London', 'Moscow'))

    def test_direct_flight(self):
        self.character.set_location('Moscow')
        self.character.action_count = 4
        self.game.draw_card(self.character)
        card = self.character.hand[0]

        success = self.character.direct_flight('Moscow', card.name)
        self.assertTrue(success)
        self.assertIn(card, self.game.player_deck.discard)
        self.assertNotIn(card, self.character.hand)
        self.assertEqual(card.name, self.character.location.name)
        self.assertEqual(3, self.character.action_count)

        success = self.character.direct_flight('London', 'Brighton')
        self.assertFalse(success)
        self.assertEqual(1, len(self.game.player_deck.discard))
        self.assertIn(card, self.game.player_deck.discard)
        self.assertEqual(3, self.character.action_count)
        self.assertEqual(card.name, self.character.location.name)

    def test_check_cure_disease(self):
        for i in range(9):
            self.game.draw_card(self.character)
        location = self.game.city_map['London']
        self.character.set_location('London')

        card_names = ['Oxford', 'Cambridge', 'Brighton', 'Southampton',
                      'Bristol']
        self.assertFalse(self.character.check_cure_disease(*card_names))

        location.has_lab = True
        self.assertFalse(self.character.check_cure_disease(*card_names))

        self.character.action_count = 4
        self.assertTrue(self.character.check_cure_disease(*card_names))

        card_names[3] = 'Moscow'
        self.assertFalse(self.character.check_cure_disease(*card_names))

        card_names[3] = 'Oxford'
        self.assertFalse(self.character.check_cure_disease(*card_names))

    def test_cure_disease(self):
        for i in range(9):
            self.game.draw_card(self.character)
        location = self.game.city_map['London']
        self.character.set_location('London')

        self.game.diseases['Blue'].cured = False
        location.has_lab = True
        self.character.action_count = 4
        card_names = ['Cambridge', 'Liverpool', 'Brighton', 'Southampton', 'Manchester']

        success = self.character.cure_disease(*card_names)
        self.assertTrue(success)
        self.assertTrue(self.game.diseases['Blue'].cured)
        self.assertEqual(3, self.character.action_count)
        for card_name in card_names:
            with self.subTest(card_name=card_name):
                self.assertFalse(self.character.hand_contains(card_name))
                self.assertTrue(any(card.name == card_name
                                    for card in self.game.player_deck.discard))

        self.assertFalse(self.character.cure_disease(*card_names))
        self.assertEqual(3, self.character.action_count)

    def test_game_won(self):
        for i in range(9):
            self.game.draw_card(self.character)
        location = self.game.city_map['London']
        self.character.set_location('London')

        self.game.diseases['Blue'].cured = False
        self.game.diseases['Black'].cured = True
        self.game.diseases['Red'].cured = True
        self.game.diseases['Yellow'].cured = True
        location.has_lab = True
        self.character.action_count = 4
        card_names = ['Cambridge', 'Liverpool', 'Brighton', 'Southampton', 'Manchester']

        with self.assertRaises(GameCrisisException):
            success = self.character.cure_disease(*card_names)

    def test_check_share_knowledge(self):
        self.character.hand = [PlayerCard('London', 'Blue'),
                               PlayerCard('Moscow', 'Black')]

        self.character.set_location('London')
        self.other_character.set_location('London')
        self.assertFalse(self.character.check_share_knowledge('London', self.other_character))

        self.character.action_count = 4
        self.assertTrue(self.character.check_share_knowledge('London', self.other_character))
        self.assertFalse(self.character.check_share_knowledge('Moscow', self.other_character))

        self.assertFalse(self.character.check_share_knowledge('London', self.character))

        self.other_character.hand.append(self.character.hand.pop(0))
        self.assertTrue(self.character.check_share_knowledge('London', self.other_character))

        self.other_character.set_location('New York')
        self.assertFalse(self.character.check_share_knowledge('London', self.other_character))

        self.character.set_location('New York')
        self.assertFalse(self.character.check_share_knowledge('New York', self.other_character))

    def test_share_knowledge(self):
        shared_card = PlayerCard('London', 'Blue')
        unshared_card = PlayerCard('Moscow', 'Black')
        self.character.hand = [shared_card, unshared_card]

        self.character.set_location('London')
        self.other_character.set_location('London')
        self.character.action_count = 4

        success = self.character.share_knowledge('London', self.other_character)
        self.assertTrue(success)
        self.assertNotIn(shared_card, self.character.hand)
        self.assertIn(shared_card, self.other_character.hand)
        self.assertEqual(3, self.character.action_count)

        success = self.character.share_knowledge('London', self.other_character)
        self.assertTrue(success)
        self.assertNotIn(shared_card, self.other_character.hand)
        self.assertIn(shared_card, self.character.hand)
        self.assertEqual(2, self.character.action_count)

        success = self.character.share_knowledge('Moscow', self.other_character)
        self.assertFalse(success)
        self.assertNotIn(unshared_card, self.other_character.hand)
        self.assertIn(unshared_card, self.character.hand)
        self.assertEqual(2, self.character.action_count)

    def test_check_treat_disease(self):
        self.game.infect_city('London', 'Blue')
        self.game.infect_city('London', 'Blue')

        self.character.set_location('London')
        self.assertFalse(self.character.check_treat_disease('Blue'))

        self.character.action_count = 4
        self.assertTrue(self.character.check_treat_disease('Blue'))
        self.assertFalse(self.character.check_treat_disease('Red'))

    def test_treat_disease_no_cure(self):
        location = self.game.city_map['London']
        self.character.set_location('London')
        self.character.action_count = 4
        location.infection_levels['Blue'] = 3
        initial_resistance = self.game.diseases['Blue'].public_health

        success = self.character.treat_disease('Blue')
        self.assertTrue(success)
        self.assertEqual(2, location.infection_levels['Blue'])
        self.assertEqual(initial_resistance + 1, self.game.diseases['Blue'].public_health)
        self.assertEqual(3, self.character.action_count)

        initial_resistance = self.game.diseases['Red'].public_health
        success = self.character.treat_disease('Red')
        self.assertFalse(success)
        self.assertEqual(2, location.infection_levels['Blue'])
        self.assertEqual(initial_resistance, self.game.diseases['Red'].public_health)
        self.assertEqual(3, self.character.action_count)

        self.character.action_count = 0
        success = self.character.treat_disease('Blue')
        self.assertFalse(success)
        self.assertEqual(2, location.infection_levels['Blue'])

    def test_treat_disease_cure(self):
        self.game.diseases['Blue'].cured = True
        location = self.game.city_map['London']
        self.character.set_location('London')
        self.character.action_count = 4
        location.infection_levels['Blue'] = 3

        success = self.character.treat_disease('Blue')
        self.assertTrue(success)
        self.assertEqual(0, location.infection_levels['Blue'])
        self.assertEqual(3, self.character.action_count)

        location.infection_levels['Blue'] = 3
        success = self.character.treat_disease('Red')
        self.assertFalse(success)
        self.assertEqual(3, location.infection_levels['Blue'])
        self.assertEqual(3, self.character.action_count)

        self.character.action_count = 0
        success = self.character.treat_disease('Blue')
        self.assertFalse(success)
        self.assertEqual(3, location.infection_levels['Blue'])

    def test_check_shuttle_flight(self):
        self.character.set_location('London')
        self.character.action_count = 4

        location = self.game.city_map['London']
        destination = self.game.city_map['Tula']
        location.has_lab = True
        destination.has_lab = True
        self.assertTrue(self.character.check_shuttle_flight('London', 'Tula'))
        self.assertFalse(self.character.check_shuttle_flight('London', 'Tver'))

        destination.has_lab = False
        self.assertFalse(self.character.check_shuttle_flight('London', 'Tula'))

        destination.has_lab = True
        self.character.set_location('New York')
        self.assertFalse(self.character.check_shuttle_flight('London', 'Tula'))

        self.character.set_location('London')
        self.character.action_count = 0
        self.assertFalse(self.character.check_shuttle_flight('London', 'Tula'))

    def test_shuttle_flight(self):
        location = self.game.city_map['London']
        destination = self.game.city_map['Tula']
        location.has_lab = True
        destination.has_lab = True
        self.character.set_location('London')
        self.character.action_count = 4

        success = self.character.shuttle_flight('London', 'Tula')
        self.assertTrue(success)
        self.assertEqual(3, self.character.action_count)
        self.assertEqual('Tula', self.character.location.name)

        success = self.character.shuttle_flight('Tula', 'Moscow')
        self.assertFalse(success)
        self.assertEqual(3, self.character.action_count)
        self.assertEqual('Tula', self.character.location.name)

    def test_check_build_lab(self):
        location = self.game.city_map['London']
        location.has_lab = False

        self.character.set_location('London')
        self.character.action_count = 4

        self.character.hand = [PlayerCard('London', 'Blue'),
                               PlayerCard('Moscow', 'Black')]

        self.assertTrue(self.character.check_build_lab())

        self.character.action_count = 0
        self.assertFalse(self.character.check_build_lab())

        self.character.action_count = 4
        location.has_lab = True
        self.assertFalse(self.character.check_build_lab())

        location.has_lab = False
        self.character.hand = []
        self.assertFalse(self.character.check_build_lab())

    def test_build_lab(self):
        location = self.game.city_map['London']
        location.has_lab = False
        card = PlayerCard('London', 'Blue')
        self.character.hand.append(card)
        self.character.set_location('London')
        self.character.action_count = 4

        success = self.character.build_lab()
        self.assertTrue(success)
        self.assertEqual(3, self.character.action_count)
        self.assertTrue(location.has_lab)
        self.assertNotIn(card, self.character.hand)
        self.assertIn(card, self.game.player_deck.discard)

        location = self.game.city_map['Moscow']
        lab_status = location.has_lab
        card = PlayerCard('Moscow', 'Black')
        self.character.hand.append(card)
        self.character.set_location('Moscow')
        self.character.action_count = 0

        success = self.character.build_lab()
        self.assertFalse(success)
        self.assertIn(card, self.character.hand)
        self.assertNotIn(card, self.game.player_deck.discard)
        self.assertEqual(0, self.character.action_count)
        self.assertEqual(lab_status, location.has_lab)

    def test_check_standard_move(self):
        self.character.set_location('London')
        self.character.action_count = 4

        self.assertTrue(self.character.check_standard_move('London', 'Brighton'))
        self.assertFalse(self.character.check_standard_move('Brighton', 'London'))
        self.assertFalse(self.character.check_standard_move('London', 'Tula'))

        self.character.action_count = 0
        self.assertFalse(self.character.check_standard_move('London', 'Brighton'))

    def test_standard_move(self):
        self.character.set_location('London')
        self.character.action_count = 4

        success = self.character.standard_move('London', 'Brighton')
        self.assertTrue(success)
        self.assertEqual(3, self.character.action_count)
        self.assertEqual('Brighton', self.character.location.name)

        success = self.character.standard_move('New York', 'London')
        self.assertFalse(success)
        self.assertEqual(3, self.character.action_count)
        self.assertEqual('Brighton', self.character.location.name)

        success = self.character.standard_move('Brighton', 'New York')
        self.assertFalse(success)
        self.assertEqual(3, self.character.action_count)
        self.assertEqual('Brighton', self.character.location.name)

        self.character.action_count = 0
        success = self.character.standard_move('Brighton', 'London')
        self.assertFalse(success)
        self.assertEqual('Brighton', self.character.location.name)
