# coding: utf-8
import unittest
from unittest import TestCase, skip, expectedFailure

import os.path as op

from src.controller import MainController


INPUT_LOCATION = op.join(op.dirname(__file__), 'test_input.txt')


# TODO: expand test case for controller
class MainControllerTestCase(TestCase):
    def test_run(self):
        self.controller = MainController(INPUT_LOCATION, 42)
        self.controller.run()

