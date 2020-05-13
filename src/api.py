# coding: utf-8
from enum import Enum


class CommandTypes(Enum):
    EMPTY = 'empty'
    CHECK = 'check'
    COMMAND = 'command'


class ResponseTypes(Enum):
    EMPTY = 'empty'
    MESSAGE = 'message'
    TERMINATION = 'termination'
