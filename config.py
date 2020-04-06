# coding: utf-8
import os
from configparser import ConfigParser


ROOT_DIR = os.path.dirname(__file__)
SETTINGS_DEFAULT_LOCATION = os.path.join(ROOT_DIR, 'settings.cfg')


def get_settings(settings_location=None):
    if settings_location is None:
        settings_location = SETTINGS_DEFAULT_LOCATION

    app_config = ConfigParser()
    app_config.read(settings_location)

    return app_config

