# coding: utf-8
import os
from configparser import ConfigParser


ROOT_DIR = os.path.join(os.path.dirname(__file__), os.pardir)
SETTINGS_DEFAULT_LOCATION = os.path.join(ROOT_DIR, 'settings.cfg')

_CACHED_SETTINGS = None


def get_settings(settings_location=None, *, refresh=False):
    global _CACHED_SETTINGS

    if refresh or _CACHED_SETTINGS is None:
        refresh_settings(settings_location)

    app_config = _CACHED_SETTINGS
    return app_config


def refresh_settings(settings_location=None):
    global _CACHED_SETTINGS

    if settings_location is None:
        settings_location = SETTINGS_DEFAULT_LOCATION

    app_config = ConfigParser()
    app_config.read(settings_location)

    _CACHED_SETTINGS = app_config

