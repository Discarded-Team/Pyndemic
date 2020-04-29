# coding: utf-8
import sys
import itertools as its
import random
import logging

from game import *
from city import NoCityCubesException
from player import LastDiseaseCuredException
import log
from commands import COMMANDS
from api import ConsoleInputManager as input_manager


class Controller:
    def run_game(self, input_file=None):

        if input_file is not None:
            self.input_manager = input_manager('file', input_file)
        else:
            self.input_manager = input_manager()

        logging.info(
            'Game started for 4 players.')

        random.seed(42)

        self.player_names = names = ['Alpha', 'Bravo', 'Charlie', 'Delta']
        self.players = players = {name: Player(name) for name in names}

        game = self.game = Game()

        for p in names:
            game.add_player(players[p])

        game.setup_game()
        game.start_game()

        try:
            self.game_cycle()
        except (NullDiseaseCapacityException, ExhaustedPlayerDeckException,
                DeathOutbreakLevelException) as e:
            logging.warning(e)
            logging.warning('Game lost!')
        except LastDiseaseCuredException as e:
            logging.warning(e)
            logging.warning('Game won!')
        except KeyboardInterrupt:
            logging.warning(
                'You decided to exit the game...')

        logging.info('---<<< Thats all! >>>---')

    def game_cycle(self):
        name_cycle = its.cycle(self.player_names)
        game = self.game

        while True:
            player = self.player = self.players[next(name_cycle)]
            logging.info(
                f'Active player: {player.name}')

            game.start_turn(player)

            while player.action_count:
                logging.info(
                    f'Actions left: {player.action_count}')
                print('Type your command:')

                command = self.input_manager.input()
                if not command:
                    continue

                logging.debug(
                    'Player action: ' + command)
                command = command.split()

                chosen_executor = None
                for executor in COMMANDS:
                    potential_executor = executor(game, player, self)
                    if potential_executor.check_valid_command(command):
                        chosen_executor = potential_executor
                        break
                if not chosen_executor:
                    logging.error(
                        'Command cannot be parsed. Type a correct command.')
                    continue

                try:
                    success = chosen_executor.execute(command)
                except NoCityCubesException as e:
                    logging.error(e)
                    success = False
                if not success:
                    logging.error(
                        'Command cannot be executed. Type some other command.')
                continue

                logging.info(
                    'Command successfully executed.')

            logging.info(
                'No actions left. Now getting cards...')

            # TODO: this must be a game method
            for i in range(2):
                game.draw_card(player)

            logging.info(
                'Cards drawn. Now starting infect phase.')

            game.infect_city_phase()

            logging.info(
                'Infect phase gone. Starting new turn.')


if __name__ == '__main__':
    input_file = sys.argv[1] if sys.argv[1:] else None
    Controller().run_game(input_file)

