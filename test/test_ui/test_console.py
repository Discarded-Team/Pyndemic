import unittest

import os.path as op
import os
import sys

from pyndemic.ui.console import ConsoleIO, ConsoleUI

INPUT_LOCATION = op.join(op.dirname(__file__), 'test_input.txt')

class ConsoleIOCase(unittest.TestCase):
    pass

class ConsoleUICase(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()
