import unittest
from unittest.mock import Mock
from pyndemic.controller import AbstractController

from pyndemic.commands import *


class MockController(AbstractController):
    def __init__(self):
        pass


class CommandTestCase(unittest.TestCase):
    def setUp(self):
        self.game = Mock()
        self.controller = MockController()
        self.character = Mock()
        self.command = Command(self.game, self.character, self.controller)

    def test_check_valid_command(self):
        # empty argument
        response = self.command.check_valid_command("")
        self.assertFalse(response)

        # irrelevant command
        command = {
            'command': 'move',
            'args'   : {}
        }
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # It is not possible to test minimal number of arguments -- the generic
        # class has none.


class MoveCommandTestCase(unittest.TestCase):
    def standard_move(self, location_name, destination_name):
        self.called = 'character.standard_move'
        return True

    def setUp(self):
        self.game = Mock()
        self.game.city_map = ['Moscow', 'Karlmarxstadt']
        self.controller = MockController()
        self.character = Mock()
        self.character.standard_move = self.standard_move

        self.command = MoveCommand(self.game, self.character, self.controller)

    def test_check_valid_command(self):
        # empty argument
        response = self.command.check_valid_command("")
        self.assertFalse(response)

        # irrelevant command
        command = {
            'command': 'fly',
            'args'   : {}
        }
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # too few arguments
        command = {
            'command': 'move',
            'args': {}
        }

        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # wrong destination
        command = {
            'command': 'move',
            'args': {
                'destination': 'London'
            }
        }

        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # wrong destination
        command = {
            'command': 'move',
            'args': {
                'destination': 'London'
            }
        }

        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # correct destination
        command = {
            'command': 'move',
            'args': {
                'destination': 'Karlmarxstadt'
            }
        }

        response = self.command.check_valid_command(command)
        self.assertTrue(response)

    def test_execute(self):
        # valid command
        command = {
            'command': 'move',
            'args': {
                'destination': 'Karlmarxstadt'
            }
        }
        response = self.command.execute(command)
        self.assertTrue(response)
        self.assertEqual(self.called, 'character.standard_move')

