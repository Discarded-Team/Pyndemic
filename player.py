# coding: utf-8


class Player:
    def __init__(self, name):
        self.game = None
        self.location = None
        self.action_count = 0
        self.hand = []
        self.name = name
        self.controller = None

    def get_distance_from_lab(self):
        self.game.set_lab_distances()
        return self.location.distance

    def get_card(self, card_name):
        for card in self.hand:
            if card.name == card_name:
                return card

    # TODO: check the real need in this method
    def set_location(self, new_location):
        self.location = self.game.city_map.get(new_location)

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
            return True
        return False

    def check_direct_flight(self, location, destination):
        if self.action_count > 0 and self.location.name == location:
            if self.handContains(destination):
                return True
        return False

    def direct_flight(self, location, destination):
        if self.check_direct_flight(location, destination):
            self.discard_card(destination)
            self.set_location(destination)
            self.action_count -= 1
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
                self.location.remove_all_cubes(colour)
            else:
                self.location.remove_cube(colour)
            self.action_count -= 1
            return True
        return False

    def check_cure_disease(self, card1, card2, card3, card4, card5):
        card_list = [card1, card2, card3, card4, card5]
        if self.action_count > 0 and self.location.has_lab:
            # TODO: check that Game Controller class provides method for
            # checking card colours
            all_one_colour = self.game.all_one_colour(card_list)
            all_in_hand = all(self.hand_contains(card) for card in card_list)
            if all_in_hand and all_one_colour:
                return True
        return False

    def cure_disease(self, card1, card2, card3, card4, card5):
        if self.check_cure_disease(card1, card2, card3, card4, card5):
            self.game.diseases[self.get_card(card1).colour].cured = True
            self.action_count -= 1
            return True
        return False

    def check_share_knowledge(self, card, player):
        if self.action_count > 0:
            if self.location.name == player.location.name:
                # FIXME: check if we use card or its name attribute here
                if self.location.name == card:
                    return True
        return False

    def share_knowledge(self, card, player):
        if self.check_share_knowledge(card, player):
            held_card = card
            # FIXME: check if we use card or its name attribute here
            player.add_card(held_card)
            self.hand.remove(held_card)
            self.action_count -= 1
            return True
        return False

    def add_card(self, new_card):
        self.hand.append(new_card)

    def discard_card(self, to_discard):
        # FIXME: check if we use card or its name attribute here
        if self.hand_contains(to_discard):
            self.hand.remove(to_discard)
            self.game.player_deck.add_discard(to_discard)
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
            return True
        return False

    def get_inputs(self):
        pass

