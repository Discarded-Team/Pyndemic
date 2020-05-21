import logging


class Command:
    command = None
    min_arguments = 0

    def __init__(self, game, character, controller):
        self.game = game
        self.character = character
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
        character = self.character
        location = character.location.name
        destination = command[1]

        success = character.standard_move(location, destination)
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
        character = self.character
        location = character.location.name
        destination = command[1]

        success = character.direct_flight(location, destination)
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
        character = self.character
        location = character.location.name
        destination = command[1]

        success = character.charter_flight(location, destination)
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
        character = self.character
        location = character.location.name
        destination = command[1]

        success = character.shuttle_flight(location, destination)
        return success


class BuildCommand(Command):
    command = 'build'
    min_arguments = 0

    def check_arguments(self, command):
        return True

    def execute(self, command):
        character = self.character

        success = character.build_lab()
        return success


class TreatCommand(Command):
    command = 'treat'
    min_arguments = 1

    def check_arguments(self, command):
        colour = command[1]
        location = self.character.location
        if colour not in location.infection_levels:
            return False
        return True

    def execute(self, command):
        character = self.character
        colour = command[1]

        success = character.treat_disease(colour)
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
        character = self.character
        card_names = command[1:6]

        success = character.cure_disease(*card_names)
        return success


class ShareCommand(Command):
    command = 'share'
    min_arguments = 2

    def check_arguments(self, command):
        card_name = command[1]
        if card_name not in self.game.city_map:
            return False

        character_name = command[2]
        if character_name not in self.controller.character_names:
            return False
        if character_name == self.character.name:
            return False

        return True

    def execute(self, command):
        character = self.character
        card_name = command[1]
        other_character = self.controller.characters[command[2]]

        success = character.share_knowledge(card_name, other_character)
        return success


class PassCommand(Command):
    command = 'pass'

    def check_arguments(self, command):
        return True

    def execute(self, command):
        character = self.character
        character.action_count = 0

        logging.info(
            f'{character}: made magic pass.')

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
