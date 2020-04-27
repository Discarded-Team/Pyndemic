# coding: utf-8
import logging

from exceptions import GameCrisisException


class LastDiseaseCuredException(GameCrisisException):
    def __str__(self):
        return 'All diseases have been cured!'


class Player:
    def __init__(self, name):
        self.game = None
        self.location = None
        self.action_count = 0
        self.hand = []
        self.name = name
        self.controller = None
        logging.debug(
            f'Created {self}')

    def __str__(self):
        return f'Player "{self.name}"'

    def info(self):
        result = f'Player {self.name}'
        if self.location is not None:
            result += f' (stays at: {self.location.name}).'

        return result

    def get_distance_from_lab(self):
        self.game.set_lab_distances()
        return self.location.distance

    def get_card(self, card_name):
        for card in self.hand:
            if card.name == card_name:
                return card
        raise ValueError(
            f"No such card in {self.name} player's hand: {card_name}.")

    def set_location(self, new_location):
        self.location = self.game.city_map[new_location]
        logging.debug(
            f'{self}: changed location to {new_location}.')

    def check_charter_flight(self, location, destination):
        if self.action_count > 0 and self.location.name == location:
            if self.hand_contains(location):
                return True
        return False

    def charter_flight(self, location, destination):
        if self.check_charter_flight(location, destination):
            self.discard_card(location)
            self.set_location(destination)
            self.action_count -= 1
            logging.info(
                (f'{self}: Performed charter flight from {location} to '
                 f'{destination}.'))
            return True
        return False

    def check_direct_flight(self, location, destination):
        if self.action_count > 0 and self.location.name == location:
            if self.hand_contains(destination):
                return True
        return False

    def direct_flight(self, location, destination):
        if self.check_direct_flight(location, destination):
            self.discard_card(destination)
            self.set_location(destination)
            self.action_count -= 1
            logging.info(
                (f'{self}: Performed direct flight from {location} to '
                 f'{destination}.'))
            return True
        return False

    def check_build_lab(self):
        if self.action_count > 0 and not self.location.has_lab:
            if self.hand_contains(self.location.name):
                return True
        return False

    def build_lab(self):
        if self.check_build_lab():
            self.discard_card(self.location.name)
            self.location.build_lab()
            self.action_count -= 1
            logging.info(
                f'{self}: Built laboratory in {self.location}.')
            return True
        return False

    def check_shuttle_flight(self, location, destination):
        if self.action_count > 0 and self.location.name == location:
            if self.location.has_lab and self.game.city_map.get(destination).has_lab:
                return True
        return False

    def shuttle_flight(self, location, destination):
        if self.check_shuttle_flight(location, destination):
            self.set_location(destination)
            self.action_count -= 1
            logging.info(
                (f'{self}: Performed shuttle flight from {location} to '
                 f'{destination}.'))
            return True
        return False

    def check_treat_disease(self, colour):
        if self.action_count > 0:
            if self.location.cubes.get(colour, 0) > 0:
                return True
        return False

    def treat_disease(self, colour):
        if self.check_treat_disease(colour):
            if self.game.diseases[colour].cured:
                dropped_cubes = self.location.remove_all_cubes(colour)
                self.game.disease_cubes[colour] += dropped_cubes
                logging.info(
                    (f'{self}: Treated {colour} disease in {self.location} '
                     f'(effectively).'))
            else:
                self.location.remove_cube(colour)
                self.game.disease_cubes[colour] += 1
                logging.info(
                    f'{self}: Treated {colour} disease in {self.location}.')
            self.action_count -= 1
            logging.info(
                (f'Now {self.location} has {self.location.cubes[colour]} '
                 f'level of {colour} disease.'))
            logging.debug(
                (f'{colour} disease capacity is now '
                 f'{self.game.disease_cubes[colour]}.'))

            return True
        return False

    def check_cure_disease(self, card1, card2, card3, card4, card5):
        card_list = [card1, card2, card3, card4, card5]
        if len(set(card_list)) != 5:
            return False
        if self.action_count > 0 and self.location.has_lab:
            all_one_colour = self.game.all_one_colour(card_list)
            all_in_hand = all(self.hand_contains(card) for card in card_list)
            if all_in_hand and all_one_colour:
                return True
        return False

    def cure_disease(self, card1, card2, card3, card4, card5):
        if self.check_cure_disease(card1, card2, card3, card4, card5):
            colour = self.get_card(card1).colour
            self.game.diseases[colour].cured = True
            card_list = [card1, card2, card3, card4, card5]
            for card in card_list:
                self.discard_card(card)
            self.action_count -= 1
            logging.info(
                f'{self}: Cured {colour} disease in {self.location}.')

            if self.game.all_diseases_cured():
                raise LastDiseaseCuredException

            return True
        return False

    def check_share_knowledge(self, card_name, player):
        if player is self:
            return False

        no_actions = self.action_count == 0
        different_locations = self.location.name != player.location.name
        card_mismatch = card_name != player.location.name
        if no_actions or different_locations or card_mismatch:
            return False

        if self.hand_contains(card_name) or player.hand_contains(card_name):
            return True
        return False

    def share_knowledge(self, card_name, player):
        if self.check_share_knowledge(card_name, player):
            transfer_forward = True
            try:
                held_card = self.get_card(card_name)
            except ValueError:
                held_card = player.get_card(card_name)
                transfer_forward = False
            if transfer_forward:
                player.add_card(held_card)
                self.hand.remove(held_card)
            else:
                self.add_card(held_card)
                player.hand.remove(held_card)
            self.action_count -= 1
            logging.info(
                f'{self}: Shared knowledge {held_card} with {player}.')

            return True
        return False

    def add_card(self, new_card):
        self.hand.append(new_card)
        logging.debug(
            f'{self}: Received new {new_card}.')

    def discard_card(self, to_discard):
        if self.hand_contains(to_discard):
            card_to_discard = self.get_card(to_discard)
            self.hand.remove(card_to_discard)
            self.game.player_deck.add_discard(card_to_discard)
            logging.info(
                f'{self}: discarded {card_to_discard}.')

            return True
        return False

    def hand_contains(self, card_name):
        return any(card.name == card_name for card in self.hand)

    def check_standard_move(self, location, destination):
        self.game.set_city_distance_name(destination)
        if self.action_count > 0 and self.location.name == location:
            if self.location.distance == 1:
                return True
        return False

    def standard_move(self, location, destination):
        if self.check_standard_move(location, destination):
            self.set_location(destination)
            self.action_count -= 1
            logging.info(
                (f'{self}: Performed standard move from {location} to '
                 f'{destination}.'))

            return True
        return False

    def check_long_move(self, location, destination):
        self.game.set_city_distance_name(destination)
        if self.location.name == location:
            if self.action_count >= self.location.distance:
                return True
        return False

    def long_move(self, location, destination):
        if self.check_long_move(location, destination):
            self.action_count -= self.location.distance
            self.set_location(destination)
            logging.info(
                (f'{self}: Performed long move from {location} to '
                 f'{destination}.'))

            return True
        return False

