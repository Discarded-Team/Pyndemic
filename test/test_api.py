# coding: utf-8
import unittest
from unittest import TestCase, skip, expectedFailure
from unittest.mock import patch

import os.path as op

from src.api import ConsoleInputManager, FileInputManager, HybridInputManager


INPUT_LOCATION = op.join(op.dirname(__file__), 'test_input.txt')


class ConsoleInputManagerTestCase(TestCase):
    input_example = ['command one', 'command two']
    
    @patch('builtins.input', side_effect=input_example)
    def test_call(self, mock_input):
        self.input = ConsoleInputManager()

        for command in self.input_example:
            with self.subTest(command=command):
                input_command = self.input()
                self.assertEqual(command, input_command)


class FileInputManagerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.input_file = INPUT_LOCATION

        with open(cls.input_file, 'r') as fin:
            cls.commands = fin.readlines()

    def setUp(self):
        self.input = FileInputManager(self.input_file)

    def test_init(self):
        reversed_command_list = list(reversed(self.commands))
        self.assertEqual(reversed_command_list, self.input._cached)

    def test_call(self):
        first_commands = [line.rstrip() for line in self.commands[:10]]

        for command in first_commands:
            with self.subTest(command=command):
                input_command = self.input()
                self.assertEqual(command, input_command)

        with self.assertRaises(IndexError):
            while True:
                command = self.input()


class HybridInputManagerTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.input_file = INPUT_LOCATION

        with open(cls.input_file, 'r') as fin:
            cls.file_commands = fin.readlines()

    def setUp(self):
        self.input = HybridInputManager('file', self.input_file)

    def test_init(self):
        self.input = HybridInputManager('console', self.input_file)
        self.assertIsInstance(self.input.input, ConsoleInputManager)

        self.input = HybridInputManager('file', self.input_file)
        self.assertIsInstance(self.input.input, FileInputManager)

    @patch('builtins.input', return_value='console input')
    def test_call(self, mock_input):
        for command in self.file_commands:
            with self.subTest(command=command):
                input_command = self.input()
                self.assertEqual(command.rstrip(), input_command)
         
        for i in range(10):       
            with self.subTest(i=i):
                input_command = self.input()
                self.assertEqual('console input', input_command)

