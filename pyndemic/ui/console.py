"""Console User Interface for Pyndemic"""
import sys
from queue import Queue

from ..core import api
from ..core.api import RequestTypes, ResponseTypes, GameplayCommands


class ConsoleUI:
    def __init__(self, controller):
        self.io = ConsoleIO()
        self.controller = controller
        self.last_ui_command = None
        self.last_ui_command_args = None
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
                    request = self.parse_user_input(request)
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

        if self.last_ui_command in CLI_COMMANDS:

            if self.last_ui_command == 'chars' or \
                    self.last_ui_command == 'characters':
                self._chars_ui_command(response)

            elif self.last_ui_command == 'hand':
                self._hand_ui_command(response)

            elif self.last_ui_command == 'labs':
                self._labs_ui_command(response)

            elif self.last_ui_command == 'infection':
                self._infection_ui_command(response)

            elif self.last_ui_command == 'position':
                self._chars_ui_command(response)
                self._labs_ui_command(response)

            elif self.last_ui_command == 'discard':
                self._discard_ui_command(response)

            self.last_ui_command = None
            self.last_ui_command_args = None

        if 'message_list' in response:
            io_response = '\n'.join(response['message_list'])
            self.io.send(io_response)
        if 'message' in response:
            io_response = response['message']
            self.io.send(io_response)

    def _chars_ui_command(self, response):
        characters = response['game_data']['characters']
        for ch in characters:
            output = "Player {}:\tin {}".format(ch['name'],
                                                ch['location'])
            self.io.send(output)
        self.io.send("\n")

    def _hand_ui_command(self, response):
        ac_name = response['game_data']['active_character']
        characters = response['game_data']['characters']
        # getting active character subtree
        ac_info = list(filter(lambda x: x['name'] == ac_name,
                              characters))[0]
        hand = ac_info['hand']

        self.io.send("\nPlayer {} hand:\n======================\n".format(
            ac_name
        ))
        for card in hand:
            # TODO this potentially will break for a non-city card
            output = "{}:\t{}".format(card['name'], card['colour'])
            self.io.send(output)
        self.io.send("======================\n")

    def _labs_ui_command(self, response):
        city_list = response['game_data']['cities']
        labs = []
        for city_name, city in city_list.items():
            if city['has_lab'] == True:
                # leave this as is if one would like to tweak the format
                labs.append("{}".format(city_name))

        if len(labs) == 0:
            self.io.send("No labs has been built\n")
        else:
            self.io.send("\nLabs are in:")
            self.io.send("\n".join(labs))
            self.io.send("\n")  # produces two lines for some reason

    def _infection_ui_command(self, response):
        infection_rate = response['game_data']['infection_rate']
        epidemic_count = response['game_data']['epidemic_count']
        outbreak_count = response['game_data']['outbreak_count']

        diseases = response['game_data']['diseases']
        disease_names = sorted((diseases.keys()))
        city_dict = response['game_data']['cities']
        city_names = sorted((city_dict.keys()))

        break_length = 56
        # total stats section
        self.io.send("\nInfection status\n" + "=" * break_length)
        self.io.send("Epidemic count {}".format(epidemic_count))
        self.io.send("Disease spreads {} cities each time".
                     format(infection_rate))
        self.io.send("{} outbreaks so far".format(outbreak_count))
        self.io.send("=" * break_length)

        header_output = "\t\t\t" + "\t".join(disease_names)
        self.io.send(header_output)
        self.io.send("-" * break_length)

        # disease status section
        infect_lvl_output = "Public Health\t"
        cured_output = "Cured?\t\t"
        for d in disease_names:
            infect_lvl_output += "\t{}".format(
                diseases[d]['public_health'])
            cured_output += "\t{}".format(
                diseases[d]['cured'])
        self.io.send(infect_lvl_output)
        self.io.send(cured_output)
        self.io.send("-" * break_length)

        # city infection status section
        for c in city_names:
            city_output = c
            total_disease = 0 # clean city filter
            if len(c) < 8: # fix for names that are too short
                city_output += "\t"
            city_output += "\t"
            for d in disease_names:
                lvl_output = city_dict[c]['infection_levels'][d]
                total_disease += lvl_output
                # better visibility for other numbers in the table
                if lvl_output == 0:
                    lvl_output = "."
                city_output += "\t{}".format(lvl_output)
            if total_disease > 0:
                self.io.send(city_output)

        self.io.send("=" * break_length + "\n")

    def _discard_ui_command(self, response):
        player_d = response['game_data']['player_deck_discard']
        infect_d = response['game_data']['infect_deck_discard']
        break_length = 56

        self.io.send("\nDiscards:\n" + "=" * break_length)
        # player deck
        self.io.send("Player cards")
        if len(player_d) == 0:
            self.io.send("Nothing is here")
        else:
            for c in player_d:
                name = c['name']
                if len(name) < 8:
                    name += "\t"
                self.io.send("{}\t{}".format(name, c['colour']))
        self.io.send("-" * break_length)

        # infect deck
        self.io.send("Infect cards")
        if len(infect_d) == 0:
            self.io.send("Nothing is here")
        else:
            for c in infect_d:
                name = c['name']
                if len(name) < 8:
                    name += "\t"
                self.io.send("{}\t{}".format(name, c['colour']))
        self.io.send("=" * break_length)


    def parse_user_input(self, input_request):
        input_request = input_request.split()
        if input_request[0] == 'quit':
            return api.termination_request()

        if input_request[0] in CLI_COMMANDS:
            self.last_ui_command = input_request[0]
            if len(input_request) > 1:
                self.last_ui_command_args = input_request[1:]
            # TODO: this request can be cached
            #  Every controller command includes game state in the response
            request = {'type': RequestTypes.CHECK}
            return request

        else:
            request = {
                'type': RequestTypes.COMMAND,
                'command': input_request[0],
                'args': {},
            }
            command_update_method = update_command[request['command']]
            command_update_method(request, input_request)

            return request


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
}


CLI_COMMANDS = ['chars', 'characters',
                'hand',
                'labs',
                'infection',
                'position',
                'discard']

