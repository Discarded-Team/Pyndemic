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
    def test_run(self):
        stdout, sys.stdout = sys.stdout, open(os.devnull, 'w')
        try:
            with sys.stdout:
                main([INPUT_LOCATION, 42])
        finally:
            sys.stdout = stdout
