from unittest import TestCase
from unittest.mock import MagicMock
from .test_helpers import construct_mock_context

from pyndemic.action_card import (GovernmentGrantActionCard,
                                  OneQuietNightActionCard)


class GovernmentGrantActionCardCase(TestCase):
    def setUp(self):
        self._ctx = construct_mock_context()
        self.mock_game = self._ctx['controller']().game

    def test_init(self):
        card = GovernmentGrantActionCard()
        self.assertEqual('Government Grant', card.name)
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
        self.mock_game.city_map["London"].build_lab.assert_called()


class OneQuietNightActionCardCase(TestCase):
    def setUp(self):
        self._ctx = construct_mock_context()
        self.mock_game = self._ctx['controller']().game

    def test_init(self):
        card = OneQuietNightActionCard()
        self.assertEqual('One Quiet Night', card.name)
        self.assertIsNone(card.colour)

    def test_check_playable(self):
        card = OneQuietNightActionCard()
        playable = card.check_playable()
        self.assertTrue(playable)

    def test_on_play(self):
        card = OneQuietNightActionCard()
        self.mock_game.skip_infect_phase = False
        card.on_play()
        mode = self.mock_game.skip_infect_phase
        self.assertTrue(mode)

    def integration_test(self):
        #TODO a comprehensive test is needed, with an actual Game
        pass

