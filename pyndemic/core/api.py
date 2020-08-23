from .utils import StringEnum


class RequestTypes(StringEnum):
    EMPTY = 'empty'
    CHECK = 'check'
    COMMAND = 'command'
    MESSAGE = 'message'
    TERMINATION = 'termination'


class ResponseTypes(StringEnum):
    EMPTY = 'empty'
    MESSAGE = 'message'
    TERMINATION = 'termination'


class GameplayCommands(StringEnum):
    MOVE = 'move'
    FLY = 'fly'
    CHARTER = 'charter'
    SHUTTLE = 'shuttle'
    BUILD = 'build'
    TREAT = 'treat'
    CURE = 'cure'
    SHARE = 'share'
    PASS = 'pass'
    CARD_GRANT = 'card_grant'
    CARD_NIGHT = 'card_night'


def termination_request():
    request = {
        'type': RequestTypes.TERMINATION,
    }
    return request


def empty_response():
    response = {
        'type': ResponseTypes.EMPTY,
    }
    return response


def final_response(message=None):
    response = {
        'type': ResponseTypes.TERMINATION,
        'message': message,
    }

    return response


def message_response(message):
    response = {
        'type': ResponseTypes.MESSAGE,
        'message': message,
    }

    return response
