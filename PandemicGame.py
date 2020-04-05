# coding: utf-8
from configparser import ConfigParser

from city import City
from card import Card
from deck import Deck
from disease import Disease
from player import Player
from ai import AIController


class PandemicGame:
    def __init__(self):
        self.starting_epidemics = None
        self.outbreak_count = 0
        self.game_over = False
        self.game_won = False
        self.disease_cubes = {}
        self.city_map = {}
        self.player_deck = Deck()
        self.infect_deck = Deck()
        self.infection_rate = None
        self.infection_rates = []
        self.epidemic_count = 0
        self.diseases = {}
        self.players = []
        self.turn_number = None

    def setup_game(self, settings_location):
        City.set_cube_colours(settings_location)
        self.get_infection_rate(settings_location)
        self.get_new_cities(settings_location)
        self.get_new_decks(settings_location)
        self.get_new_diseases(settings_location)
        self.set_starting_epidemics(settings_location)
        for player in self.players:
            # TODO: simplify this line
            player.set_location(list(self.city_map.keys())[0])
        AIController.number_AI = 0

    def set_starting_epidemics(self, settings_location):
        parser = ConfigParser()
        parser.read(settings_location)
        self.starting_epidemics = int(parser.get('Diseases', 'epidemics'))

    def start_game(self):
        self.shuffle_decks()
        self.inital_infect_phase()
        self.draw_inital_hands()
        self.add_epidemics()

    def add_epidemics(self):
        self.player_deck.add_epidemics(self.starting_epidemics)

    def add_player(self, new_player):
        new_player.game = self
        new_player.controller = AIController(new_player)
        self.players.append(new_player)

    def draw_card(self, player_drawing):
        drawn_card = self.player_deck.take_top_card()
        if drawn_card.name == 'Epidemic':
            self.epidemic_phase()
        else:
            player_drawing.add_card(drawn_card)

    def shuffle_decks(self):
        self.infect_deck.shuffle()
        self.player_deck.shuffle()

    def has_x_cube_city(self, x):
        return any(city.get_max_cubes() == x
                   for city in self.city_map.values())

    def get_count_x_cube_city(self, x):
        count_x_cities = 0
        for city in self.city_map.values():
            if city.get_max_cubes() == x:
                count_x_cities += 1
        return count_x_cities

    def infect_city(self, city, colour):
        infected_city = self.city_map.get(city)
        if infected_city.cubes[colour] < 3:
            infected_city.add_cube(colour)
            self.disease_cubes[colour] -= 1
        else:
            self.outbreak(city, colour)

    def outbreak(self, city, colour):
        # TODO FIXME: avoid outbreak recursion for cities
        outbreak_city = self.city_map.get(city)
        self.outbreak_count += 1
        for connected_city in outbreak_city.connected_cities:
            self.infect_city(connected_city.name, colour)

    def inital_infect_phase(self):
        cubes_to_add = 3
        for i in range(3):
            for j in range(3):
                drawn_card = self.infect_deck.take_top_card()
                self.infect_deck.add_discard(drawn_card)
                for k in range(cubes_to_add):
                    self.infect_city(drawn_card.name, drawn_card.colour)
            cubes_to_add -= 1

    def infect_city_phase(self):
        for i in range(int(self.infection_rate)):
            drawn_card = self.infect_deck.take_top_card()
            self.infect_deck.add_discard(drawn_card)
            infected_city = self.city_map.get(drawn_card.name)
            self.infect_city(infected_city.name, infected_city.colour)

    def start_turn(self, player):
        player.action_count = 4
        # TODO

    def epidemic_phase(self):
        drawn_card = self.infect_deck.take_bottom_card()
        self.infect_deck.add_discard(drawn_card)
        city_epidemic = self.city_map.get(drawn_card.name)
        for i in range(3):
            # TODO: stop infecting in case of outbreak
            self.infect_city(city_epidemic.name, city_epidemic.colour)
        self.infect_deck.shuffle_discard_to_top()
        self.increment_epidemic_count()

    def get_new_cities(self, settings_location):
        parser = ConfigParser()
        parser.read(settings_location)
        number_of_cities = int(parser.get('Cities', 'number'))
        for i in range(1, number_of_cities + 1):
            city_name = parser.get('Cities', "city" + str(i))
            city_colour = parser.get('Colours', "city" + str(i))
            self.city_map[city_name] = City(city_name, city_colour)
        self.make_cities(settings_location)

    def new_infect_deck(self, settings_location):
        parser = ConfigParser()
        parser.read(settings_location)
        number_of_cards = int(parser.get('Cities', 'number'))
        for i in range(1, number_of_cards + 1):
            city_name = parser.get('Cities', "city" + str(i))
            city_colour = parser.get('Colours', "city" + str(i))
            new_card = Card(city_name, city_colour)
            self.infect_deck.add_card(new_card)

    def new_player_deck(self, settings_location):
        parser = ConfigParser()
        parser.read(settings_location)
        number_of_cards = int(parser.get('Cities', 'number'))
        for i in range(1, number_of_cards + 1):
            city_name = parser.get('Cities', "city" + str(i))
            city_colour = parser.get('Colours', "city" + str(i))
            new_card = Card(city_name, city_colour)
            self.player_deck.add_card(new_card)

    def get_new_decks(self, settings_location):
        self.new_infect_deck(settings_location)
        self.new_player_deck(settings_location)

    def get_new_diseases(self, settings_location):
        parser = ConfigParser()
        parser.read(settings_location)
        number_of_disease = int(parser.get('Diseases', 'number'))
        for i in range(1, number_of_disease + 1):
            disease_colour = parser.get('Diseases', 'disease' + str(i))
            self.diseases[disease_colour] = Disease(disease_colour)
            num_cubes = int(parser.get('Diseases', 'cubes'))
            self.disease_cubes[disease_colour] = num_cubes

    def make_cities(self, settings_location):
        parser = ConfigParser()
        parser.read(settings_location)
        for city_name, city in self.city_map.items():
            connections = parser.get('Connections', city_name)
            usedlist = connections.split()
            for x in usedlist:
                added_city_name = parser.get('Cities', "city" + x)
                city.add_connection(self.city_map[added_city_name])

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
        currentDistance = starting_cities[0].distance
        for city in starting_cities:
            for connected_city in city.connected_cities:
                if connected_city.distance == 999:
                    updated_cities.append(connected_city)
                    connected_city.distance = current_distance + 1
        if updated_cities:
            self.update_distances(updated_cities)

    def increment_epidemic_count(self):
        self.epidemic_count += 1
        self.infection_rate = self.infection_rates[self.epidemic_count]

    def get_infection_rate(self, settings_location):
        parser = ConfigParser()
        parser.read(settings_location)
        self.infection_rates = parser.get('Diseases', 'rate')
        self.infection_rate = int(self.infection_rates[0])

    def draw_inital_hands(self):
        num_cards_by_players = {4: 2, 3: 3, 2: 4}
        num_players = len(self.players)
        cards_to_draw = num_cards_by_players[num_players]

        for player in self.players:
            for i in range(cards_to_draw):
                player.add_card(self.player_deck.take_top_card())

