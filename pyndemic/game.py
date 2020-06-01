import logging

from collections import OrderedDict

from . import config
from .exceptions import GameCrisisException
from .core import GameEntity
from .city import City
from .deck import PlayerDeck, InfectDeck
from .disease import Disease


class ExhaustedPlayerDeckException(GameCrisisException):
    def __str__(self):
        return 'Player deck exhausted!'


class DeathOutbreakLevelException(GameCrisisException):
    def __str__(self):
        return 'Number of outbreaks reached death level!'


class Game(GameEntity):
    def __init__(self):
        self.starting_epidemics = None
        self.outbreak_count = 0
        self.game_over = False
        self.game_won = False
        self.city_map = OrderedDict()
        self.infection_rate = None
        self.infection_rates = []
        self.epidemic_count = 0
        self.diseases = {}
        self.characters = []
        self.turn_number = None
        self.outbreak_stack = set()
        self.settings = None

    def setup_game(self, settings_location=None):
        self.settings = config.get_settings(settings_location)
        self.get_infection_rate()
        self.get_new_diseases()
        self.get_new_city_map()
        self.player_deck = PlayerDeck()
        self.infect_deck = InfectDeck()
        self.get_new_decks()
        self.set_starting_epidemics()

        self.emit_signal('Game ready to begin.')
        self.emit_signal(
            f'Difficulty level: {self.starting_epidemics} Epidemics.',
        )

    def start_game(self):
        self.shuffle_decks()
        self.initial_infect_phase()
        self.draw_initial_hands()
        self.add_epidemics()
        self.emit_signal('Game started.')

        initial_city = self.settings['Other']['initial_city']
        for character in self.characters:
            character.set_location(initial_city)
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
        self.emit_signal(
            f'Added {self.starting_epidemics} Epidemics to a character deck.',
        )

    def add_character(self, new_character):
        new_character.game = self
        self.characters.append(new_character)
        self.emit_signal(
            f'Added new {new_character}.',
        )

    def draw_card(self, character_drawing):
        try:
            drawn_card = self.player_deck.take_top_card()
        except IndexError:
            raise ExhaustedPlayerDeckException

        if drawn_card.name == 'Epidemic':
            self.emit_signal(
                f'{character_drawing} drew Epidemic!',
            )

            self.epidemic_phase()
        else:
            character_drawing.add_card(drawn_card)
            self.emit_signal(
                f'{character_drawing} got {drawn_card}.',
            )

    def shuffle_decks(self):
        self.infect_deck.shuffle()
        self.player_deck.shuffle()
        self.emit_signal('Decks shuffled.')

    # TODO: Extend this method for arbitrary change of levels
    def infect_city(self, city_name, colour):
        infected_city = self.city_map.get(city_name)
        self.emit_signal(
            f'Infecting {infected_city} with {colour} disease.',
        )

        if infected_city.infection_levels[colour] < 3:
            self.diseases[colour].decrease_resistance(1)
            infected_city.increase_infection_level(colour)
            self.emit_signal(
                (f'Infected {infected_city} with {colour} disease (reached '
                 f'level {infected_city.infection_levels[colour]}).'),
            )

        else:
            self.emit_signal(
                (f'{infected_city} has already maximum {colour} disease '
                 'level. Outbreak is coming!'),
            )
            self.outbreak(city_name, colour)

    def outbreak(self, city_name, colour):
        outbreak_city = self.city_map.get(city_name)
        if city_name in self.outbreak_stack:
            return

        self.emit_signal(
            f'Starting outbreak in {outbreak_city} ({colour} disease).',
        )
        self.outbreak_stack.add(city_name)
        self.outbreak_count += 1
        self.emit_signal(
            f'Outbreak level is now {self.outbreak_count}.',
        )
        if self.outbreak_count == 8:
            raise DeathOutbreakLevelException

        for connected_city in outbreak_city.connected_cities:
            if connected_city in self.outbreak_stack:
                continue
            self.infect_city(connected_city.name, colour)

    def initial_infect_phase(self):
        self.emit_signal('Starting initial infect phase.')
        levels_to_add = 3
        for i in range(3):
            for j in range(3):
                drawn_card = self.infect_deck.take_top_card()
                self.infect_deck.add_discard(drawn_card)
                for k in range(levels_to_add):
                    self.infect_city(drawn_card.name, drawn_card.colour)
            levels_to_add -= 1
        self.emit_signal('Initial infect phase finished.')

    def infect_city_phase(self):
        self.outbreak_stack.clear()
        self.emit_signal(
            f'Starting infect phase ({self.infection_rate} cities to infect).',
        )

        for i in range(self.infection_rate):
            drawn_card = self.infect_deck.take_top_card()
            self.infect_deck.add_discard(drawn_card)
            infected_city = self.city_map.get(drawn_card.name)
            self.infect_city(infected_city.name, infected_city.colour)
            # TODO test that outbreak stack is cleared after each drawn card
            self.outbreak_stack.clear()

        self.emit_signal('Infect phase finished.')

    def start_turn(self, character):
        character.action_count = 4
        self.emit_signal(
            f'{character} now plays.',
        )
        # TODO test?

    def end_turn(self, character):
        self.emit_signal('No actions left. Now getting cards...')

        for i in range(2):
            self.draw_card(character)

        self.emit_signal('Cards drawn. Now starting infect phase.')

        self.infect_city_phase()
        self.emit_signal('Infect phase gone. Starting new turn.')
        # TODO test ?

    def epidemic_phase(self):
        self.emit_signal('Starting epidemic phase.')
        self.increment_epidemic_count()

        drawn_card = self.infect_deck.take_bottom_card()
        self.infect_deck.add_discard(drawn_card)
        city_epidemic = self.city_map.get(drawn_card.name)
        self.emit_signal(
            f'Starting epidemic in {city_epidemic}.',
        )
        for i in range(3):
            self.infect_city(city_epidemic.name, city_epidemic.colour)
            if city_epidemic in self.outbreak_stack:
                break
        self.infect_deck.shuffle_discard_to_top()
        self.emit_signal('Infect discard shuffled and returned to deck.')
        self.emit_signal('Epidemic phase finished.')

    def set_starting_epidemics(self):
        self.starting_epidemics = self.settings['Other'].getint('epidemics')
        logging.debug(
            f'Set difficulty level to {self.starting_epidemics}.')

    def get_new_city_map(self):
        self.create_cities()
        self.connect_cities()
        logging.debug('Created city graph.')

    def get_new_decks(self):
        self.player_deck.prepare(self.city_map.values())
        self.infect_deck.prepare(self.city_map.values())
        logging.debug('Decks prepared.')

    def get_new_diseases(self):
        diseases_section = self.settings['Diseases']
        max_resistance = self.settings['Other'].getint('max_resistance')

        for disease_id in diseases_section:
            disease_colour = diseases_section[disease_id]
            self.diseases[disease_colour] = \
                Disease(disease_colour, max_resistance)

    def create_cities(self):
        cities_section = self.settings['Cities']
        city_colours_section = self.settings['City Colours']
        disease_colours = list(self.diseases.keys())

        for city_id in cities_section:
            city_name = cities_section[city_id]
            city_colour = city_colours_section[city_id]
            new_city = City(city_name, city_colour)
            new_city.init_colours(disease_colours)
            self.city_map[city_name] = new_city

    def connect_cities(self):
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

    def increment_epidemic_count(self):
        self.epidemic_count += 1
        self.infection_rate = int(self.infection_rates[self.epidemic_count])
        self.emit_signal(
            f'Incremented infection rate (now {self.infection_rate}).',
        )

    def draw_initial_hands(self):
        num_cards_by_characters = {4: 2, 3: 3, 2: 4}
        num_characters = len(self.characters)
        cards_to_draw = num_cards_by_characters[num_characters]
        self.emit_signal(
            f'Draw initial character cards ({cards_to_draw} per character).',
        )

        for character in self.characters:
            for i in range(cards_to_draw):
                self.draw_card(character)
