# coding: utf-8
import unittest
from unittest import TestCase, skip, expectedFailure

import os.path as op

import config


SETTINGS_LOCATION = op.join(op.dirname(__file__), 'test_settings.cfg')


class ConfigModuleTestCase(TestCase):
    def setUp(self):
        config._CACHED_SETTINGS = None

    def tearDown(self):
        config._CACHED_SETTINGS = None

    def test_refresh_settings(self):
        config.refresh_settings(SETTINGS_LOCATION)
        settings = config._CACHED_SETTINGS

        self.assertIsNotNone(settings)
        self.assertEqual('Tianjin', settings['Cities']['city21'])
        self.assertEqual(['20', '22', '23'], settings['Connections']['Tianjin'].split())
        self.assertEqual('Red', settings['City Colours']['city21'])
        self.assertEqual('Black', settings['Diseases']['disease4'])
        self.assertEqual('2222334', settings['Other']['rate'])

    def test_get_settings(self):
        settings = config.get_settings(SETTINGS_LOCATION)

        self.assertIsNotNone(config._CACHED_SETTINGS)
        self.assertIs(config._CACHED_SETTINGS, settings)

        settings_again = config.get_settings(SETTINGS_LOCATION)
        self.assertIs(settings, settings_again)

        settings_reloaded = config.get_settings(SETTINGS_LOCATION, refresh=True)
        self.assertIs(config._CACHED_SETTINGS, settings_reloaded)
        self.assertIsNot(settings_reloaded, settings)
        self.assertEqual(settings['Cities']['city9'],
                         settings_reloaded['Cities']['city9'])

