from unittest import TestCase
from unittest.mock import MagicMock
from .test_helpers import construct_mock_context

from pyndemic.action_card import (GovernmentGrantActionCard,
                                  QuietNightActionCard)


class GovernmentGrantActionCardCase(TestCase):
    def setUp(self):
        self._ctx = construct_mock_context()
        self.mock_game = self._ctx['controller']().game

    def test_init(self):
        card = GovernmentGrantActionCard()
        self.assertEqual("Government Grant", card.name)
        self.assertIsNone(card.colour)

    def test_check_playable(self):
        card = GovernmentGrantActionCard()

        self.mock_game.city_map = {}
        playable = card.check_playable("London")
        self.assertFalse(playable)

        self.mock_game.city_map["London"] = MagicMock()
        self.mock_game.city_map["London"].has_lab = True
        playable = card.check_playable("London")
        self.assertFalse(playable)

        self.mock_game.city_map["London"] = MagicMock()
        self.mock_game.city_map["London"].has_lab = False
        playable = card.check_playable("London")
        self.assertTrue(playable)

    def test_on_play(self):
        card = GovernmentGrantActionCard()
        self.mock_game.city_map = {"London": MagicMock()}
        self.mock_game.city_map["London"].has_lab = False
        result = card.on_play("London")
        self.assertTrue(result)


class QuietNightActionCardCase(TestCase):
    def setUp(self):
        self._ctx = construct_mock_context()
        self.mock_game = self._ctx['controller']().game

    def test_init(self):
        card = QuietNightActionCard()
        self.assertEqual("Quiet Night", card.name)
        self.assertIsNone(card.colour)

    def test_check_playable(self):
        card = QuietNightActionCard()
        playable = card.check_playable()
        self.assertTrue(playable)

    def test_on_play(self):
        card = QuietNightActionCard()
        self.mock_game.infect_phase_mode = "normal"
        card.on_play()
        mode = self.mock_game.infect_phase_mode
        self.assertEqual("skip for the next player", mode)

    def integration_test(self):
        #TODO a comprehensive test is needed, with actual Game and Controller
        pass

