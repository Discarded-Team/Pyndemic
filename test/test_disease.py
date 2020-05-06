# coding: utf-8

from unittest import TestCase, skip, expectedFailure

from src.disease import Disease, NoHealthException


class DiseaseTestCase(TestCase):
    def test_init(self):
        disease = Disease('Blue', 42)
        self.assertEqual('Blue', disease.colour)
        self.assertEqual(42, disease.public_health)
        self.assertFalse(disease.cured)

    def test_decrease_resistance(self):
        disease = Disease('Blue', 42)
        disease.decrease_resistance(10)
        self.assertEqual(32, disease.public_health)
        with self.assertRaises(NoHealthException):
            disease.decrease_resistance(40)

    def test_increase_resistance(self):
        disease = Disease('Blue', 10)
        disease.increase_resistance(10)
        self.assertEqual(20, disease.public_health)
