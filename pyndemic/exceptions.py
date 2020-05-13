# coding: utf-8


class GameException(Exception):
    """Raised by regular game incidents that do not affect game continuity.

    E.g., this can be a trying to make impossible action, or this can be an
    signal to play the effect of some action immediately.
    """
    pass


class GameCrisisException(Exception):
    """Raised by conditions that can potentially stop the game according to
    game rules, such as game winning/losing conditions.
    """
    pass

