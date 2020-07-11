from unittest import TestCase, skip
from unittest.mock import patch, Mock, MagicMock

from io import StringIO
import os.path as op

from pyndemic.deck import ExhaustedPlayerDeckException
from pyndemic.character import LastDiseaseCuredException
from pyndemic.core import api
from pyndemic.ui.console import ConsoleUI
from pyndemic.controller import GameController
from pyndemic.core.context import _ContextManager


INPUT_LOCATION = op.join(op.dirname(__file__), 'test_input.txt')


class GameControllerTestCase(TestCase):
    def setUp(self):
        self.controller = GameController(random_state=42)

    def tearDown(self):
        del self.controller

    def test_init(self):
        self.assertTrue(hasattr(self.controller, '_ctx'))
        ctx = self.controller._ctx
        ctx_id = ctx['id']
        self.assertIn(ctx_id, _ContextManager._contexts)
        self.assertIs(ctx, _ContextManager._contexts[ctx_id])
        self.assertIs(self.controller, ctx['controller']())

    @patch('pyndemic.controller.Game')
    def test_start_game(self, game_class):
        singleton_game_instance = MagicMock()
        game_class.return_value = singleton_game_instance

        self.controller.setup({'players': ['A', 'B']})
        self.controller.start_game()

        # test that Game setup methods called
        self.assertIs(singleton_game_instance, self.controller.game)
        singleton_game_instance.setup_game.assert_called()
        singleton_game_instance.start_game.assert_called()

        # test that character list is filled
        self.assertEqual(["A", "B"], list(self.controller.character_names))

    @patch('pyndemic.controller.Game')
    def test_send(self, game_class):
        with patch("pyndemic.controller.GameController.emit_signal") as emit:
            self.controller.setup({'players': ['A', 'B']})
            self.controller.start_game()
            self.controller._loop = Mock()

            # test LastDiseaseCuredException
            self.controller._loop.send = Mock(
                side_effect=LastDiseaseCuredException)
            request = {'type': 'message', 'message': 'some text'}
            result = self.controller.send(request)
            emit.assert_any_call(str(LastDiseaseCuredException()),
                                 log_level=30)

            # test GameCrisisException
            self.controller._loop.send = Mock(
                side_effect=ExhaustedPlayerDeckException)
            request = {'type': 'message', 'message': 'some text'}
            result = self.controller.send(request)
            emit.assert_any_call(str(ExhaustedPlayerDeckException()),
                                 log_level=30)
            # some message
            expected_response = {'type': 'message', 'message': "send it back"}
            self.controller._loop.send = Mock(side_effect=[expected_response])
            request = {'type': 'message', 'message': 'some text'}
            result = self.controller.send(request)
            self.assertEqual(expected_response, result)

            # termination
            request = {'type': api.RequestTypes.TERMINATION,
                       'message': 'some text'}
            result = self.controller.send(request)
            self.assertEqual(api.RequestTypes.TERMINATION, result['type'])

            # check
            request = {'type': api.RequestTypes.CHECK,
                       'message': 'some text'}
            result = self.controller.send(request)
            self.assertEqual(api.RequestTypes.MESSAGE, result['type'])
            self.assertEqual("", result['message'])

    @patch('pyndemic.controller.Game')
    def test_switch_player(self, game_class):
        self.controller.setup({'players': ['A', 'B']})
        self.controller.start_game()
        active_player = self.controller.current_character
        self.controller._switch_character()
        new_player = self.controller.current_character

        self.assertNotEqual(new_player, active_player)
        self.assertIsInstance(self.controller.game.active_character, str)
        self.assertEqual(new_player.name, self.controller.game.active_character)


# TODO: expand test case, remove the hardcoded exit message
# TODO: skip because adding ActionCards ruins card sequence
# One needs to reconstruct after all cards were added
@skip
class GameRunTestCase(TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stdin.readline', side_effect=open(INPUT_LOCATION, 'r'))
    def test_game_session(self, mock_input, mock_stdout):
        random_state = 42
        controller = GameController(random_state=random_state)
        ui = ConsoleUI(controller=controller)
        ui.run()

        received_output = mock_stdout.getvalue().split("\n")
        self.assertEqual("Finishing program...", received_output[-2])
