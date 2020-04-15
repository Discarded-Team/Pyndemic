# coding: utf-8
import itertools


AI_DISTANCE_TO_BUILD = 5
AI_NAME_PREFIX = "AIController"


class AIController:
    number_AI = 0

    def __init__(self, player):
        __class__.number_AI += 1
        self.name = AI_NAME_PREFIX + str(__class__.number_AI)
        self.player = player
        self.distance_to_build = AI_DISTANCE_TO_BUILD

    def cure_possible(self):
        hand_combinations = self.hand_combinations(self.player.hand)
        for hand in hand_combinations:
            if self.player.check_cure_disease(hand[0], hand[1], hand[2], hand[3], hand[4]):
                return True
        return False

    # TODO: make a seperate function of it
    def hand_combinations(self, current_hand):
        card_names = []
        for card in current_hand:
            card_names.append(card.name)
        if len(current_hand) > 4:
            possible_hands = itertools.combinations(card_names, 5)
        return possible_hands

    def build_lab_sensible(self):
        self.player.game.set_lab_distances()
        if self.player.get_distance_from_lab() > self.distance_to_build:
            if self.player.hand_contains(self.player.location.name):
                return True
        return False

