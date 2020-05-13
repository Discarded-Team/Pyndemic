# coding: utf-8
import unittest
from unittest import TestCase, skip, expectedFailure
from unittest.mock import patch

import os.path as op


INPUT_LOCATION = op.join(op.dirname(__file__), 'test_input.txt')
