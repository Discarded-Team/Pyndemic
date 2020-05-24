"""Console User Interface for Pyndemic"""
import sys
from queue import Queue

from .. import api
from ..api import CommandTypes, ResponseTypes, GameplayCommands


class ConsoleUI:
    def __init__(self, controller):
        self.io = ConsoleIO()
        self.controller = controller

        self.termination_step = None

    def run(self):
        self.termination_step = False
        with self.io, self.controller:
            while True:
                self.io.send('Waiting for command...')
                try:
                    command = self.io.listen()
                except KeyboardInterrupt:
                    self.io.send('You decided to exit the game...')
                    command = 'quit'

                if not command:
                    continue

                try:
                    command = parse_command(command)
                except LookupError:
                    controller_response = api.message_response(
                        'ERROR: this command cannot be parsed. '
                        'Type a correct command.')
                else:
                    controller_response = self.controller.send(command)

                response = self.process_response(controller_response)
                self.io.send(response)

                if self.termination_step:
                    self.io.send('Finishing program...')
                    break

    def process_response(self, response):
        if response['type'] == ResponseTypes.TERMINATION.value:
            self.termination_step = True

        response = response['message'] if 'message' in response else None

        return response


class ConsoleIO:
    def __init__(self):
        self.responses = Queue()

    def __enter__(self):
        self.run()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def run(self):
        pass

    def stop(self):
        self.flush_output()

    def listen(self):
        request = sys.stdin.readline().rstrip()
        return request

    def send(self, response):
        if response:
            self.responses.put(response)
        self.flush_output()

    def flush_output(self):
        while not self.responses.empty():
            response = self.responses.get()
            print(response, flush=True)


def parse_command(input_command):
    input_command = input_command.split()
    if input_command[0] == 'quit':
        return api.termination_command()

    command = {
        'type': CommandTypes.COMMAND.value,
        'command': input_command[0],
        'args': {},
    }
    command_update_method = update_command[command['command']]
    command_update_method(command, input_command)

    return command


def _update_move_command(command, input_command):
    command['args'] = {
        'destination': input_command[1],
    }


def _update_no_args_command(command, input_command):
    pass


def _update_treat_command(command, input_command):
    command['args'] = {
        'colour': input_command[1],
    }


def _update_cure_command(command, input_command):
    command['args'] = {
        'cards': input_command[1:],
    }


def _update_share_command(command, input_command):
    command['args'] = {
        'card': input_command[1],
        'player': input_command[2],
    }


update_command = {
    GameplayCommands.MOVE.value: _update_move_command,
    GameplayCommands.FLY.value: _update_move_command,
    GameplayCommands.CHARTER.value: _update_move_command,
    GameplayCommands.SHUTTLE.value: _update_move_command,
    GameplayCommands.BUILD.value: _update_no_args_command,
    GameplayCommands.TREAT.value: _update_treat_command,
    GameplayCommands.CURE.value: _update_cure_command,
    GameplayCommands.SHARE.value: _update_share_command,
    GameplayCommands.PASS.value: _update_no_args_command,
}
