# coding: utf-8
import unittest
from unittest import TestCase, skip, expectedFailure

from card import Card, PlayerCard, InfectCard


class CardTestCase(TestCase):
    def test_init(self):
        card = Card('London', 'Blue')
        self.assertEqual('London', card.name)
        self.assertEqual('Blue', card.colour)

