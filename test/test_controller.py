from unittest import TestCase, skip
from unittest.mock import patch

from io import StringIO
import os.path as op

from pyndemic.ui.console import ConsoleUI
from pyndemic.controller import GameController

INPUT_LOCATION = op.join(op.dirname(__file__), 'test_input.txt')


# TODO: expand test case, remove the hardcoded exit message
class GameControllerTestCase(TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stdin.readline', side_effect=open(INPUT_LOCATION, 'r'))
    def test_game_session(self, mock_input, mock_stdout):
        random_state = 42
        controller = GameController(random_state=random_state)
        ui = ConsoleUI(controller=controller)
        ui.run()

        received_output = mock_stdout.getvalue().split("\n")
        self.assertEqual("Finishing program...", received_output[-2])
