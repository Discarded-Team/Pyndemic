# coding: utf-8
import unittest
from unittest import TestCase, skip, expectedFailure

from disease import Disease


class DiseaseTestCase(TestCase):
    def test_init(self):
        disease = Disease('Blue')
        self.assertEqual('Blue', disease.colour)
        self.assertFalse(disease.cured)

