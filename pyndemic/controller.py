import itertools as its
import random

from abc import ABC, abstractmethod

from .game import *
from .city import NoDiseaseInCityException
from .character import LastDiseaseCuredException, Character
from . import log
from .commands import COMMANDS
from . import api


class AbstractController(ABC):
    def __enter__(self):
        self.run()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    @abstractmethod
    def run(self):
        pass

    def stop(self):
        self._loop.close()

    def send(self, command):
        return self._loop.send(command)

    def throw(self, exception):
        self._loop.throw(exception)


class GameController(AbstractController):
    def __init__(self, random_state=None):
        self.game = None
        self.characters = {}
        self.current_character = None
        self.name_cycle = None
        self._loop = None

        if random_state is not None:
            random.seed(random_state)
            logging.info(
                f'Random state is fixed ({random_state})')

    @property
    def character_names(self):
        return self.characters.keys()

    def run(self):
        self.start_game(['Alpha', 'Bravo', 'Charlie', 'Delta'])
        self._loop = self.game_loop()
        self._loop.send(None)

    def start_game(self, character_names):
        logging.info(
            f'Starting game for {len(character_names)} players.')

        self.characters = {name: Character(name) for name in character_names}
        self.name_cycle = its.cycle(self.character_names)

        self.game = Game()
        for character in self.characters.values():
            self.game.add_character(character)

        self.game.setup_game()
        self.game.start_game()
        self._switch_character()

    def send(self, command):
        if command == 'quit':
            return api.final_response('---<<< That\'s all! >>>---')
        try:
            return self._loop.send(command)
        except LastDiseaseCuredException as e:
            logging.warning(e)
            logging.warning('Game won!')
        except GameCrisisException as e:
            logging.warning(e)
            logging.warning('Game lost!')

        return api.final_response('---<<< That\'s all! >>>---')

    def game_loop(self):
        response = None
        while True:
            command = yield response
            if not command:
                response = api.empty_response()
                continue

            self.run_single_command(command)
            response = api.empty_response()

    def run_single_command(self, command):
        logging.debug(
            'Character action: ' + command)
        command = command.split()

        for executor_class in COMMANDS:
            executor = executor_class(self.game, self.current_character, self)
            if executor.check_valid_command(command):
                break
        else:
            logging.error(
                'Command cannot be parsed. Type a correct command.')
            return

        try:
            success = executor.execute(command)
        except NoDiseaseInCityException as e:
            logging.error(e)
            success = False
        if not success:
            logging.error(
                'Command cannot be executed. Type some other command.')

        if self.current_character.action_count == 0:
            self.game.end_turn(self.current_character)
            self._switch_character()
        else:
            logging.info(
                f'Actions left: {self.current_character.action_count}')

    def _switch_character(self):
        self.current_character = self.characters[next(self.name_cycle)]
        logging.info(
            f'Active player: {self.current_character.name}')

        self.game.start_turn(self.current_character)
        logging.info(
            f'Actions left: {self.current_character.action_count}')
