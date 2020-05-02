# coding: utf-8

from unittest import TestCase, skip, expectedFailure

from src.disease import Disease, NullDiseaseCapacityException


class DiseaseTestCase(TestCase):
    def test_init(self):
        disease = Disease('Blue', 42)
        self.assertEqual('Blue', disease.colour)
        self.assertEqual(42, disease.cubes_at_bank)
        self.assertFalse(disease.cured)

    def test_take_cubes_from_bank(self):
        disease = Disease('Blue', 42)
        disease.take_cubes_from_bank(10)
        self.assertEqual(32, disease.cubes_at_bank)
        with self.assertRaises(NullDiseaseCapacityException):
            disease.take_cubes_from_bank(40)

    def test_put_cubes_to_bank(self):
        disease = Disease('Blue', 10)
        disease.put_cubes_to_bank(10)
        self.assertEqual(20, disease.cubes_at_bank)
