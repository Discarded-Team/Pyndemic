from enum import Enum


class CommandTypes(Enum):
    EMPTY = 'empty'
    CHECK = 'check'
    COMMAND = 'command'
    MESSAGE = 'message'
    TERMINATION = 'termination'


class ResponseTypes(Enum):
    EMPTY = 'empty'
    MESSAGE = 'message'
    TERMINATION = 'termination'


class GameplayCommands(Enum):
    MOVE = 'move'
    FLY = 'fly'
    CHARTER = 'charter'
    SHUTTLE = 'shuttle'
    BUILD = 'build'
    TREAT = 'treat'
    CURE = 'cure'
    SHARE = 'share'
    PASS = 'pass'


def termination_command():
    command = {
        'type': CommandTypes.TERMINATION.value,
    }
    return command


def empty_response():
    response = {
        'type': ResponseTypes.EMPTY.value,
    }
    return response


def final_response(message=None):
    response = {
        'type': ResponseTypes.TERMINATION.value,
        'message': message,
    }

    return response


def message_response(message):
    response = {
        'type': ResponseTypes.MESSAGE.value,
        'message': message,
    }

    return response