from enum import Enum


class CommandTypes(Enum):
    EMPTY = 'empty'
    CHECK = 'check'
    COMMAND = 'command'
    MESSAGE = 'message'


class ResponseTypes(Enum):
    EMPTY = 'empty'
    MESSAGE = 'message'
    TERMINATION = 'termination'
