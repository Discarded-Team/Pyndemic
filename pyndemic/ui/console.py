"""Console User Interface for Pyndemic"""
import sys
from queue import Queue

from ..core import api
from ..core.api import RequestTypes, ResponseTypes, GameplayCommands


class ConsoleUI:
    def __init__(self, controller):
        self.io = ConsoleIO()
        self.controller = controller

        self.termination_step = None

    def run(self):
        self.termination_step = False
        with self.io, self.controller:
            request = {'type': RequestTypes.CHECK}
            check_response = self.controller.send(request)
            self.process_response(check_response)

            while True:
                if self.termination_step:
                    self.io.send('Finishing program...')
                    break

                self.io.send('Waiting for command...')
                try:
                    request = self.io.listen()
                except KeyboardInterrupt:
                    self.io.send('You decided to exit the game...')
                    request = 'quit'

                if not request:
                    continue

                try:
                    request = parse_request(request)
                except LookupError:
                    controller_response = api.message_response(
                        'ERROR: this command cannot be parsed. '
                        'Type a correct command.')
                else:
                    controller_response = self.controller.send(request)

                self.process_response(controller_response)

    def process_response(self, response):
        if response['type'] == ResponseTypes.TERMINATION:
            self.termination_step = True

        if 'message_list' in response:
            io_response = '\n'.join(response['message_list'])
            self.io.send(io_response)
        if 'message' in response:
            io_response = response['message']
            self.io.send(io_response)


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


def parse_request(input_request):
    input_request = input_request.split()
    if input_request[0] == 'quit':
        return api.termination_request()

    request = {
        'type': RequestTypes.COMMAND,
        'command': input_request[0],
        'args': {},
    }
    command_update_method = update_command[request['command']]
    command_update_method(request, input_request)

    return request


def _update_move_command(request, input_request):
    request['args'] = {
        'destination': input_request[1],
    }


def _update_no_args_command(request, input_request):
    pass


def _update_treat_command(request, input_request):
    request['args'] = {
        'colour': input_request[1],
    }


def _update_cure_command(request, input_request):
    request['args'] = {
        'cards': input_request[1:],
    }


def _update_share_command(request, input_request):
    request['args'] = {
        'card': input_request[1],
        'player': input_request[2],
    }


update_command = {
    GameplayCommands.MOVE: _update_move_command,
    GameplayCommands.FLY: _update_move_command,
    GameplayCommands.CHARTER: _update_move_command,
    GameplayCommands.SHUTTLE: _update_move_command,
    GameplayCommands.BUILD: _update_no_args_command,
    GameplayCommands.TREAT: _update_treat_command,
    GameplayCommands.CURE: _update_cure_command,
    GameplayCommands.SHARE: _update_share_command,
    GameplayCommands.PASS: _update_no_args_command,
    GameplayCommands.CARD_GRANT: _update_move_command,
    GameplayCommands.CARD_NIGHT: _update_no_args_command
}
