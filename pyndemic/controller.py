import itertools as its
import weakref
import random
import logging
from queue import Queue

from .game import Game, GameCrisisException
from .city import NoDiseaseInCityException
from .character import LastDiseaseCuredException, Character
from . import log
from .commands import COMMANDS
from .core import api
from .core.context import ContextRegistrationMeta


class AbstractController(metaclass=ContextRegistrationMeta,
                         ctx_name='controller'):
    """Abstract interface for all game controller classes.
    This class cannot have instances and must be inherited.
    """
    def __enter__(self):
        self.run()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def run(self):
        raise NotImplementedError

    def stop(self):
        self._loop.close()

    def send(self, command):
        return self._loop.send(command)

    def throw(self, exception):
        self._loop.throw(exception)

    def emit_signal(self, message, log_level=logging.INFO):
        if isinstance(message, str):
            signal = api.message_response(message)
        else:
            signal = message

        if log_level is not None:
            logging.log(log_level, signal)

        self.signals.put(signal)


class GameController(AbstractController):
    def __init__(self, random_state=None):
        self.game = None
        self.characters = {}
        self.current_character = None
        self.name_cycle = None
        self._loop = None
        self.signals = Queue()
        self.random_state = random_state

    @property
    def character_names(self):
        return self.characters.keys()

    def run(self):
        self.start_game(['Alpha', 'Bravo', 'Charlie', 'Delta'])
        self._loop = self.game_loop()
        self._loop.send(None)

    def start_game(self, character_names):
        self.emit_signal(
            f'Starting game for {len(character_names)} players.',
        )

        if self.random_state is not None:
            random.seed(self.random_state)
            self.emit_signal(
                f'Random state is fixed ({self.random_state})',
            )

        self.characters = {name: Character(name) for name in character_names}
        self.name_cycle = its.cycle(self.character_names)

        self.game = Game()
        for character in self.characters.values():
            self.game.add_character(character)

        self.game.setup_game()
        self.game.start_game()
        self._switch_character()

    def send(self, request):
        if request['type'] == api.RequestTypes.TERMINATION:
            return api.final_response('---<<< That\'s all! >>>---')

        if request['type'] == api.RequestTypes.CHECK:
            return api.message_response(self._flush_signals())

        try:
            response = self._loop.send(request)
            return response
        except LastDiseaseCuredException as e:
            self.emit_signal(str(e), log_level=logging.WARNING)
            self.emit_signal('Game won!', log_level=logging.WARNING)
        except GameCrisisException as e:
            self.emit_signal(str(e), log_level=logging.WARNING)
            self.emit_signal('Game lost!', log_level=logging.WARNING)

        self.emit_signal('---<<< That\'s all! >>>---')
        final_message = self._flush_signals()
        return api.final_response(final_message)

    def game_loop(self):
        response = None
        while True:
            command = yield response
            if not command:
                response = api.empty_response()
                continue

            self.run_single_command(command)
            response = api.message_response(self._flush_signals())

    def run_single_command(self, command):
        logging.debug(
            f'Character action: {command}.')

        for executor_class in COMMANDS:
            executor = executor_class(self.game, self.current_character, self)
            if executor.check_valid_command(command):
                break
        else:
            self.emit_signal(
                'Command cannot be parsed. Type a correct command.',
                log_level=logging.ERROR)
            return

        try:
            success = executor.execute(command)
        except NoDiseaseInCityException as e:
            self.emit_signal(str(e), log_level=logging.ERROR)
            success = False
        if not success:
            self.emit_signal(
                'Command cannot be executed. Type some other command.',
                log_level=logging.ERROR)

        if self.current_character.action_count == 0:
            self.game.end_turn(self.current_character)
            self._switch_character()
        else:
            self.emit_signal(
                f'Actions left: {self.current_character.action_count}',
            )

    def _switch_character(self):
        self.current_character = self.characters[next(self.name_cycle)]
        self.emit_signal(
            f'Active player: {self.current_character.name}',
        )

        self.game.start_turn(self.current_character)
        self.emit_signal(
            f'Actions left: {self.current_character.action_count}',
        )

    def _flush_signals(self):
        message_list = []
        while not self.signals.empty():
            message = self.signals.get()['message']
            message_list.append(message)

        return '\n'.join(message_list)
