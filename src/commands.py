# coding: utf-8
import logging


class Command:
    command = None
    min_arguments = 0

    def __init__(self, game, player, controller):
        self.game = game
        self.player = player
        self.controller = controller

    def check_valid_command(self, command):
        if not command or command[0] != self.command:
            return False
        if len(command[1:]) < self.min_arguments:
            return False
        if not self.check_arguments(command):
            return False
        return True


class MoveCommand(Command):
    command = 'move'
    min_arguments = 1

    def check_arguments(self, command):
        destination = command[1]
        if destination not in self.game.city_map:
            return False
        return True

    def execute(self, command):
        player = self.player
        location = player.location.name
        destination = command[1]

        success = player.standard_move(location, destination)
        return success


class FlyCommand(Command):
    command = 'fly'
    min_arguments = 1

    def check_arguments(self, command):
        destination = command[1]
        if destination not in self.game.city_map:
            return False
        return True

    def execute(self, command):
        player = self.player
        location = player.location.name
        destination = command[1]

        success = player.direct_flight(location, destination)
        return success


class CharterCommand(Command):
    command = 'charter'
    min_arguments = 1

    def check_arguments(self, command):
        destination = command[1]
        if destination not in self.game.city_map:
            return False
        return True

    def execute(self, command):
        player = self.player
        location = player.location.name
        destination = command[1]

        success = player.charter_flight(location, destination)
        return success

class ShuttleCommand(Command):
    command = 'shuttle'
    min_arguments = 1

    def check_arguments(self, command):
        destination = command[1]
        if destination not in self.game.city_map:
            return False
        return True

    def execute(self, command):
        player = self.player
        location = player.location.name
        destination = command[1]

        success = player.shuttle_flight(location, destination)
        return success


class BuildCommand(Command):
    command = 'build'
    min_arguments = 0

    def check_arguments(self, command):
        return True

    def execute(self, command):
        player = self.player

        success = player.build_lab()
        return success


class TreatCommand(Command):
    command = 'treat'
    min_arguments = 1

    def check_arguments(self, command):
        colour = command[1]
        location = self.player.location
        if colour not in location.cube_colours:
            return False
        return True

    def execute(self, command):
        player = self.player
        colour = command[1]

        success = player.treat_disease(colour)
        return success


class CureCommand(Command):
    command = 'cure'
    min_arguments = 5

    def check_arguments(self, command):
        card_names = command[1:6]
        if len(card_names) != 5:
            return False
        if any(card_name not in self.game.city_map for card_name in card_names):
            return False
        return True

    def execute(self, command):
        player = self.player
        card_names = command[1:6]

        success = player.cure_disease(*card_names)
        return success


class ShareCommand(Command):
    command = 'share'
    min_arguments = 2

    def check_arguments(self, command):
        card_name = command[1]
        if card_name not in self.game.city_map:
            return False

        player_name = command[2]
        if player_name not in self.controller.player_names:
            return False
        if player_name == self.player.name:
            return False

        return True

    def execute(self, command):
        player = self.player
        card_name = command[1]
        other_player = self.controller.players[command[2]]

        success = player.share_knowledge(card_name, other_player)
        return success


class PassCommand(Command):
    command = 'pass'

    def check_arguments(self, command):
        return True

    def execute(self, command):
        player = self.player
        player.action_count = 0

        logging.info(
            f'{player}: made magic pass.')

        return True


COMMANDS = [
    MoveCommand,
    FlyCommand,
    CharterCommand,
    ShuttleCommand,
    BuildCommand,
    TreatCommand,
    CureCommand,
    ShareCommand,
    PassCommand,
]

