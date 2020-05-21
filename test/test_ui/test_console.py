import unittest
from unittest.mock import patch
from io import StringIO

import os.path as op
from pyndemic.ui.console import ConsoleIO, ConsoleUI


INPUT_LOCATION = op.join(op.dirname(__file__), 'test_input.txt')


class ConsoleIOCase(unittest.TestCase):
    input_example = ['command one', 'command two', 'quit']

    @patch('sys.stdin.readline', side_effect=input_example)
    def test_listen(self, mock_input):
        self.input = ConsoleIO()

        for command in self.input_example:
            with self.subTest(command=command):
                input_command = self.input.listen()
                self.assertEqual(command, input_command)

    @patch('sys.stdout', new_callable=StringIO)
    @patch('sys.stdin.readline', side_effect=input_example)
    def test_context(self, mock_input, mock_stdout):
        """
        tests both context manager methods, send() and flush()
        :param mock_input:
        :param mock_stdout:
        """
        self.input = ConsoleIO()

        with self.input:
            for command in self.input_example:
                c = self.input.send(command)

        received_commands = mock_stdout.getvalue().split("\n")

        for idx, command in enumerate(self.input_example):
            with self.subTest(command=command):
                self.assertEqual(command, received_commands[idx])


# TODO: Provide tests for ConsoleUI
class ConsoleUICase(unittest.TestCase):
    pass
