# coding: utf-8
import itertools as its
import random
import logging

from .game import *
from .city import NoDiseaseInCityException
from .player import LastDiseaseCuredException
from . import log
from .commands import COMMANDS


class BaseController:
    def send(self, command):
        return self._loop.send(command)

    def throw(self, exception):
        self._loop.throw(exception)

    def empty_response(self):
        return {
            'type': 'empty',
        }

    def final_response(self, message):
        final_response = {
            'type': 'termination',
            'message': message,
        }
        return final_response


class GameController(BaseController):
    def __init__(self, random_state=None):
        self.game = None
        self.players = {}
        self.current_player = None
        self.name_cycle = None
        self._loop = None

        if random_state is not None:
            random.seed(random_state)
            logging.info(
                f'Random state is fixed ({random_state})')

    @property
    def player_names(self):
        return self.players.keys()

    def run(self):
        self.start_game(['Alpha', 'Bravo', 'Charlie', 'Delta'])
        self._loop = self.game_loop()
        self._loop.send(None)

    def start_game(self, player_names):
        logging.info(
            f'Starting game for {len(player_names)} players.')

        self.players = {name: Player(name) for name in player_names}
        self.name_cycle = its.cycle(self.player_names)

        self.game = Game()
        for player in self.players.values():
            self.game.add_player(player)

        self.game.setup_game()
        self.game.start_game()
        self._switch_player()

    def send(self, command):
        if command == 'quit':
            return self.final_response('---<<< That\'s all! >>>---')
        try:
            return self._loop.send(command)
        except LastDiseaseCuredException as e:
            logging.warning(e)
            logging.warning('Game won!')
        except GameCrisisException as e:
            logging.warning(e)
            logging.warning('Game lost!')

        return self.final_response('---<<< That\'s all! >>>---')

    def game_loop(self):
        response = None
        while True:
            command = yield response
            if not command:
                response = self.empty_response()
                continue

            self.run_single_command(command)
            response = self.empty_response()

    def run_single_command(self, command):
        logging.debug(
            'Player action: ' + command)
        command = command.split()

        for executor_class in COMMANDS:
            executor = executor_class(self.game, self.current_player, self)
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

        if self.current_player.action_count == 0:
            logging.info(
                'No actions left. Now getting cards...')
            self.end_turn()
        else:
            logging.info(
                f'Actions left: {self.current_player.action_count}')

    def end_turn(self):
        for i in range(2):
            self.game.draw_card(self.current_player)

        logging.info(
            'Cards drawn. Now starting infect phase.')

        self.game.infect_city_phase()

        logging.info(
            'Infect phase gone. Starting new turn.')

        self._switch_player()

    def _switch_player(self):
        self.current_player = self.players[next(self.name_cycle)]
        logging.info(
            f'Active player: {self.current_player.name}')

        self.game.start_turn(self.current_player)
        logging.info(
            f'Actions left: {self.current_player.action_count}')
