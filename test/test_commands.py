import unittest
from unittest.mock import Mock, MagicMock
from pyndemic.controller import AbstractController

from pyndemic.commands import *


class MockController(AbstractController):
    def __init__(self):
        self.characters = dict(Alice=1, Bob=2)
        self.character_names = ['Alice', 'Bob']


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
        command = dict(command='move', args={})
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # It is not possible to test minimal number of arguments -- the generic
        # class has none.


class MoveCommandTestCase(unittest.TestCase):
    def setUp(self):
        self.game = Mock()
        self.game.city_map = ['Yakutsk', 'Karlmarxstadt']
        self.controller = MockController()
        self.character = Mock()
        self.character.standard_move = MagicMock(return_value=True)

        self.command = MoveCommand(self.game, self.character, self.controller)

    def test_check_valid_command(self):
        # irrelevant command
        command = dict(command='fly', args={})
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # too few arguments
        command = dict(command='move', args={})
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # wrong argument
        command = dict(command='move', args={
            'colour': 'cyan'
        })
        with self.assertRaises(KeyError):
            self.command.check_valid_command(command)

        # wrong destination
        command = dict(command='move', args={
            'destination': 'London'
        })
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # correct destination
        command = dict(command='move', args={
            'destination': 'Karlmarxstadt'
        })
        response = self.command.check_valid_command(command)
        self.assertTrue(response)

    def test_execute(self):
        # valid command
        command = dict(command='move', args={
            'destination': 'Karlmarxstadt'
        })
        self.command.execute(command)
        self.character.standard_move.assert_called()


class FlyCommandTestCase(unittest.TestCase):
    def setUp(self):
        self.game = Mock()
        self.game.city_map = ['Yakutsk', 'Karlmarxstadt']
        self.controller = MockController()
        self.character = Mock()
        self.character.direct_flight = MagicMock(return_value=True)

        self.command = FlyCommand(self.game, self.character, self.controller)

    def test_check_valid_command(self):
        # irrelevant command
        command = dict(command='move', args={})
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # too few arguments
        command = dict(command='fly', args={})
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # wrong argument
        command = dict(command='fly', args={
            'colour': 'cyan'
        })
        with self.assertRaises(KeyError):
            self.command.check_valid_command(command)

        # wrong destination
        command = dict(command='fly', args={
            'destination': 'London'
        })
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # correct destination
        command = dict(command='fly', args={
            'destination': 'Karlmarxstadt'
        })
        response = self.command.check_valid_command(command)
        self.assertTrue(response)

    def test_execute(self):
        # valid command
        command = dict(command='move', args={
            'destination': 'Karlmarxstadt'
        })
        self.command.execute(command)
        self.character.direct_flight.assert_called()


class CharterCommandTestCase(unittest.TestCase):
    def setUp(self):
        self.game = Mock()
        self.game.city_map = ['Yakutsk', 'Karlmarxstadt']
        self.controller = MockController()
        self.character = Mock()
        self.character.charter_flight = MagicMock(return_value=True)

        self.command = CharterCommand(self.game, self.character,
                                      self.controller)

    def test_check_valid_command(self):
        # irrelevant command
        command = dict(command='move', args={})
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # too few arguments
        command = dict(command='charter', args={})
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # wrong argument
        command = dict(command='charter', args={
            'colour': 'cyan'
        })
        with self.assertRaises(KeyError):
            self.command.check_valid_command(command)

        # wrong destination
        command = dict(command='charter', args={
            'destination': 'London'
        })
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # correct destination
        command = dict(command='charter', args={
            'destination': 'Karlmarxstadt'
        })

        response = self.command.check_valid_command(command)
        self.assertTrue(response)

    def test_execute(self):
        # valid command
        command = dict(command='charter', args={
            'destination': 'Karlmarxstadt'
        })
        self.command.execute(command)
        self.character.charter_flight.assert_called()


class ShuttleCommandTestCase(unittest.TestCase):
    def setUp(self):
        self.game = Mock()
        self.game.city_map = ['Yakutsk', 'Karlmarxstadt']
        self.controller = MockController()
        self.character = Mock()
        self.character.shuttle_flight = MagicMock(return_value=True)

        self.command = ShuttleCommand(self.game, self.character,
                                      self.controller)

    def test_check_valid_command(self):
        # irrelevant command
        command = dict(command='move', args={})
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # too few arguments
        command = dict(command='shuttle', args={})
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # wrong argument
        command = dict(command='shuttle', args={
            'colour': 'cyan'
        })
        with self.assertRaises(KeyError):
            self.command.check_valid_command(command)

        # wrong destination
        command = dict(command='shuttle', args={
            'destination': 'London'
        })
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # correct destination
        command = dict(command='shuttle', args={
            'destination': 'Karlmarxstadt'
        })

        response = self.command.check_valid_command(command)
        self.assertTrue(response)

    def test_execute(self):
        # valid command
        command = dict(command='shuttle', args={
            'destination': 'Karlmarxstadt'
        })
        self.command.execute(command)
        self.character.shuttle_flight.assert_called()


class BuildCommandTestCase(unittest.TestCase):
    def setUp(self):
        self.game = Mock()
        self.controller = MockController()
        self.character = Mock()
        self.character.build_lab = MagicMock(return_value=True)

        self.command = BuildCommand(self.game, self.character,
                                    self.controller)

    def test_check_valid_command(self):
        # irrelevant command
        command = dict(command='move', args={})
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

    def test_execute(self):
        # valid command
        command = dict(command='build', args={})
        self.command.execute(command)
        self.character.build_lab.assert_called()


class TreatCommandTestCase(unittest.TestCase):
    def setUp(self):
        self.game = Mock()
        self.controller = MockController()
        self.character = Mock()
        self.character.treat_disease = MagicMock(return_value=True)
        self.character.location.infection_levels = ['maroon', 'cyan']

        self.command = TreatCommand(self.game, self.character,
                                    self.controller)

    def test_check_valid_command(self):
        # irrelevant command
        command = dict(command='move', args={})
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # too few arguments
        command = dict(command='treat', args={})
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # wrong argument
        command = dict(command='treat', args={
            'destination': 'Unknown'
        })
        with self.assertRaises(KeyError):
            self.command.check_valid_command(command)

        # wrong colour
        command = dict(command='treat', args={
            'colour': 'yellow'
        })
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # correct colour
        command = dict(command='treat', args={
            'colour': 'cyan'
        })
        response = self.command.check_valid_command(command)
        self.assertTrue(response)

    def test_execute(self):
        # valid command
        command = dict(command='treat', args={
            'colour': 'cyan'
        })
        self.command.execute(command)
        self.character.treat_disease.assert_called()


class CureCommandTestCase(unittest.TestCase):
    def setUp(self):
        self.game = Mock()
        self.game.city_map = ['one', 'two', 'three', 'four', 'five', 'six']
        self.controller = MockController()
        self.character = Mock()
        self.character.cure_disease = MagicMock(return_value=True)

        self.command = CureCommand(self.game, self.character,
                                   self.controller)

    def test_check_valid_command(self):
        # irrelevant command
        command = dict(command='move', args={})
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # too few arguments
        command = dict(command='cure', args={})
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # too few cards
        command = dict(command='cure', args={
            'cards': ['one', 'two', 'three', 'four']
        })
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # wrong cards
        command = dict(command='cure', args={
            'cards': ['one', 'two', 'three', 'four', 'hundred']
        })
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # correct colour
        command = dict(command='cure', args={
            'cards': ['one', 'two', 'three', 'four', 'five']
        })
        response = self.command.check_valid_command(command)
        self.assertTrue(response)

    def test_execute(self):
        # valid command
        command = dict(command='treat', args={
            'cards': ['one', 'two', 'three', 'four', 'five']
        })
        self.command.execute(command)
        self.character.cure_disease.assert_called()


class ShareCommandTestCase(unittest.TestCase):
    def setUp(self):
        self.game = Mock()
        self.game.city_map = ['one', 'two', 'three', 'four', 'five', 'six']
        self.controller = MockController()
        self.character = Mock()
        self.character.share_knowledge = MagicMock(return_value=True)
        self.character.name = 'Alice'

        self.command = ShareCommand(self.game, self.character,
                                    self.controller)

    def test_check_valid_command(self):
        # irrelevant command
        command = dict(command='move', args={})
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # too few arguments
        command = dict(command='share', args={
            'card': 'one'
        })
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # wrong argument 1
        command = dict(command='share', args={
            'destination': 'Unknown',
            'player': 'Bob'
        })
        with self.assertRaises(KeyError):
            self.command.check_valid_command(command)

        # wrong argument 2
        command = dict(command='share', args={
            'card': 'one',
            'destination': 'Unknown'
        })
        with self.assertRaises(KeyError):
            self.command.check_valid_command(command)

        # wrong card
        command = dict(command='share', args={
            'card': 'hundred',
            'player': 'Bob'
        })
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # wrong player 1
        command = dict(command='share', args={
            'card': 'one',
            'player': 'Charlie'
        })
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # wrong player 2 - to herself
        command = dict(command='share', args={
            'card': 'one',
            'player': 'Alice'
        })
        response = self.command.check_valid_command(command)
        self.assertFalse(response)

        # correct command
        command = dict(command='share', args={
            'card': 'one',
            'player': 'Bob'
        })
        response = self.command.check_valid_command(command)
        self.assertTrue(response)

    def test_execute(self):
        # valid command
        command = dict(command='share', args={
            'card': 'one',
            'player': 'Bob'
        })
        self.command.execute(command)
        self.character.share_knowledge.assert_called()
