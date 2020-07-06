import sys
import os
import logging
from logging import StreamHandler, Formatter
from logging.handlers import RotatingFileHandler

from . import config


LOG_DIR = os.path.join(config.ROOT_DIR, 'log')
LOG_FILENAME = os.path.join(LOG_DIR, 'game.log')


logger = logging.getLogger('PYNDEMIC')
logger.setLevel('DEBUG')
formatter = Formatter('%(name)s %(levelname)s: %(message)s')


settings = config.get_settings()
file_log_enabled = settings['Log'].getboolean('enable_log')


if file_log_enabled:
    os.makedirs(LOG_DIR, exist_ok=True)
    file_handler = RotatingFileHandler(LOG_FILENAME, backupCount=4, delay=True)
    file_handler.setFormatter(formatter)
    file_handler.setLevel('DEBUG')
    if os.path.exists(LOG_FILENAME):
        file_handler.doRollover()

    logger.addHandler(file_handler)


logging.root = logger
