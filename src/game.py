# coding: utf-8
import logging

from . import config
from .exceptions import GameCrisisException
from .city import City
from .card import Card
from .deck import PlayerDeck, InfectDeck
from .disease import Disease
from .player import Player


class ExhaustedPlayerDeckException(GameCrisisException):
    def __str__(self):
        return 'Player deck exhausted!'


class DeathOutbreakLevelException(GameCrisisException):
    def __str__(self):
        return 'Number of outbreaks reached death level!'


class Game:
    def __init__(self):
        self.starting_epidemics = None
        self.outbreak_count = 0
        self.game_over = False
        self.game_won = False
        self.city_map = {}
        self.player_deck = PlayerDeck()
        self.infect_deck = InfectDeck()
        self.infection_rate = None
        self.infection_rates = []
        self.epidemic_count = 0
        self.diseases = {}
        self.players = []
        self.turn_number = None
        self.outbreak_stack = set()
        logging.debug(
            'Created new game.')

    def setup_game(self, settings_location=None):
        self.settings = config.get_settings(settings_location)
        City.set_cube_colours(self.settings)
        self.get_infection_rate()
        self.get_new_cities()
        self.get_new_decks()
        self.get_new_diseases()
        self.set_starting_epidemics()

        logging.info(
            'Game ready to begin.')
        logging.info(
            f'Difficulty level: {self.starting_epidemics} Epidemics.')

    def start_game(self):
        self.shuffle_decks()
        self.inital_infect_phase()
        self.draw_initial_hands()
        self.add_epidemics()
        logging.info(
            'Game started.')

        initial_city = self.settings['Other']['initial_city']
        for player in self.players:
            player.set_location(initial_city)
        self.city_map[initial_city].has_lab = True

    # TODO: improve this method
    def all_one_colour(self, card_names):
        card_colours = {self.city_map[name].colour for name in card_names}
        one_colour = len(card_colours) == 1
        return one_colour

    def all_diseases_cured(self):
        return all(disease.cured for disease in self.diseases.values())

    def add_epidemics(self):
        self.player_deck.add_epidemics(self.starting_epidemics)
        logging.info(
            f'Added {self.starting_epidemics} Epidemics to a player deck.')

    def add_player(self, new_player):
        new_player.game = self
        self.players.append(new_player)
        logging.info(
            f'Added new {new_player}.')

    def draw_card(self, player_drawing):
        try:
            drawn_card = self.player_deck.take_top_card()
        except IndexError:
            raise ExhaustedPlayerDeckException

        if drawn_card.name == 'Epidemic':
            logging.info(
                f'{player_drawing} drew Epidemic!')
            self.epidemic_phase()
        else:
            player_drawing.add_card(drawn_card)
            logging.info(
                f'{player_drawing} got {drawn_card}.')

    def shuffle_decks(self):
        self.infect_deck.shuffle()
        self.player_deck.shuffle()
        logging.info(
            'Decks shuffled.')

    def has_x_cube_city(self, x):
        return any(city.get_max_cubes() == x
                   for city in self.city_map.values())

    def get_count_x_cube_city(self, x):
        count_x_cities = 0
        for city in self.city_map.values():
            if city.get_max_cubes() == x:
                count_x_cities += 1
        return count_x_cities

    # TODO: Extend this method for arbitrary cube number
    def infect_city(self, city, colour):
        infected_city = self.city_map.get(city)
        logging.info(
            f'Infecting {infected_city} with {colour} disease.')
        if infected_city.cubes[colour] < 3:
            self.diseases[colour].take_cubes_from_bank(1) # 1 cube
            infected_city.add_cube(colour)
            logging.info(
                (f'Infected {infected_city} with {colour} disease (reached '
                 f'level {infected_city.cubes[colour]}).'))
        else:
            logging.info(
                (f'{infected_city} has already maximum {colour} disease '
                 'level. Outbreak is coming!'))
            self.outbreak(city, colour)

    def outbreak(self, city, colour):
        outbreak_city = self.city_map.get(city)
        if city in self.outbreak_stack:
            return

        logging.info(
            f'Starting outbreak in {outbreak_city} ({colour} disease).')
        self.outbreak_stack.add(city)
        self.outbreak_count += 1
        logging.info(
            f'Outbreak level is now {self.outbreak_count}.')
        if self.outbreak_count == 8:
            raise DeathOutbreakLevelException

        for connected_city in outbreak_city.connected_cities:
            if connected_city in self.outbreak_stack:
                continue
            self.infect_city(connected_city.name, colour)

    def inital_infect_phase(self):
        logging.info(
            'Starting initial infect phase.')
        cubes_to_add = 3
        for i in range(3):
            for j in range(3):
                drawn_card = self.infect_deck.take_top_card()
                self.infect_deck.add_discard(drawn_card)
                for k in range(cubes_to_add):
                    self.infect_city(drawn_card.name, drawn_card.colour)
            cubes_to_add -= 1
        logging.info(
            'Initial infect phase finished.')

    def infect_city_phase(self):
        self.outbreak_stack.clear()
        logging.info(
            f'Starting infect phase ({self.infection_rate} cities to infect).')

        for i in range(self.infection_rate):
            drawn_card = self.infect_deck.take_top_card()
            self.infect_deck.add_discard(drawn_card)
            infected_city = self.city_map.get(drawn_card.name)
            self.infect_city(infected_city.name, infected_city.colour)
        self.outbreak_stack.clear()

        logging.info(
            'Infect phase finished.')

    def start_turn(self, player):
        player.action_count = 4
        logging.info(
            f'{player} now plays.')
        # TODO

    def epidemic_phase(self):
        logging.info(
            'Starting epidemic phase.')
        self.increment_epidemic_count()

        drawn_card = self.infect_deck.take_bottom_card()
        self.infect_deck.add_discard(drawn_card)
        city_epidemic = self.city_map.get(drawn_card.name)
        logging.info(
            f'Starting epidemy in {city_epidemic}.')
        for i in range(3):
            self.infect_city(city_epidemic.name, city_epidemic.colour)
            if city_epidemic in self.outbreak_stack:
                break
        self.infect_deck.shuffle_discard_to_top()
        logging.info(
            'Infect discard shuffled and returned to deck.')
        logging.info(
            'Epidemic phase finished.')

    def set_starting_epidemics(self):
        self.starting_epidemics = self.settings['Other'].getint('epidemics')
        logging.debug(
            f'Set difficulty level to {self.starting_epidemics}.')

    def get_new_cities(self):
        cities_section = self.settings['Cities']
        city_colours_section = self.settings['City Colours']

        for city_id in cities_section:
            city_name = cities_section[city_id]
            city_colour = city_colours_section[city_id]
            new_city = City(city_name, city_colour)
            self.city_map[city_name] = new_city

        self.make_cities()
        logging.debug(
            'Created city graph.')

    def get_new_decks(self):
        self.player_deck.prepare(self.settings)
        self.infect_deck.prepare(self.settings)
        logging.debug(
            'Decks prepared.')

    def get_new_diseases(self):
        diseases_section = self.settings['Diseases']
        number_of_cubes = self.settings['Other'].getint('cubes')

        for disease_id in diseases_section:
            disease_colour = diseases_section[disease_id]
            self.diseases[disease_colour] = Disease(disease_colour, number_of_cubes)

    def make_cities(self):
        cities_section = self.settings['Cities']
        connections = self.settings['Connections']

        for city_name, city in self.city_map.items():
            city_connections = connections.get(city_name).split()
            for id_ in city_connections:
                added_city_name = cities_section.get('city' + id_)
                city.add_connection(self.city_map[added_city_name])

    def get_infection_rate(self):
        self.infection_rates = self.settings['Other'].get('rate')
        self.infection_rate = int(self.infection_rates[0])

    def set_lab_distances(self):
        cities_with_labs = []
        for city in self.city_map.values():
            if city.has_lab:
                cities_with_labs.append(city)
        self.set_cities_distances(cities_with_labs)

    def set_cities_distances_names(self, city_names):
        cities = []
        for name in city_names:
            cities.append(self.city_map[name])
        self.set_cities_distances(cities)

    def set_cities_distances(self, cities):
        self.reset_distances()
        for city in cities:
            city.distance = 0
        self.update_distances(cities)

    def set_city_distance_name(self, city_name):
        city_list = [self.city_map[city_name]]
        self.set_cities_distances(city_list)

    def set_city_distance(self, city):
        city_list = [city]
        self.set_cities_distances(city_list)

    def reset_distances(self):
        for city in self.city_map.values():
            city.distance = 999

    def update_distances(self, starting_cities):
        updated_cities = []
        current_distance = starting_cities[0].distance
        for city in starting_cities:
            for connected_city in city.connected_cities:
                if connected_city.distance == 999:
                    updated_cities.append(connected_city)
                    connected_city.distance = current_distance + 1
        if updated_cities:
            self.update_distances(updated_cities)

    def increment_epidemic_count(self):
        self.epidemic_count += 1
        self.infection_rate = int(self.infection_rates[self.epidemic_count])
        logging.info(
            f'Incremented infection rate (now {self.infection_rate}).')

    def draw_initial_hands(self):
        num_cards_by_players = {4: 2, 3: 3, 2: 4}
        num_players = len(self.players)
        cards_to_draw = num_cards_by_players[num_players]
        logging.info(
            f'Draw initial player cards ({cards_to_draw} per player).')

        for player in self.players:
            for i in range(cards_to_draw):
                self.draw_card(player)
