# coding: utf-8
import unittest
from unittest import TestCase, skip, expectedFailure

import os.path as op
import os
import sys

from src.controller import GameController
from pyndemic import main


INPUT_LOCATION = op.join(op.dirname(__file__), 'test_input.txt')


# TODO: expand test case for controller
class GameControllerTestCase(TestCase):
    def test_game_session(self):
        stdout, sys.stdout = sys.stdout, open(os.devnull, 'w')
        stdin, sys.stdin = sys.stdin, open(INPUT_LOCATION, 'r')
        random_state = 42
        controller = GameController(random_state)

        try:
            with sys.stdout, sys.stdin, controller:
                while True:
                    command = sys.stdin.readline().rstrip()
                    response = controller.send(command)
                    if response['type'] == 'termination':
                        break
        finally:
            sys.stdout, sys.stdin = stdout, stdin
