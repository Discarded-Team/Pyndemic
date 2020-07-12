

class BaseFormatter:
    """
    Provides methods of serialisation of Game instance for various viewpoints
    """

    @classmethod
    def game_to_dict(cls, game):
        """
        :param game: Game object
        :return: dict with (almost) complete state of the game. Decks return
            only the discard.
        :characters: list of Character dicts
            :name: str
            :location: str
            :action_count: int
            :hand: list of Card dicts
                :name: str
                :colour: str
        :player_deck_discard: list of Card dicts
            :name: str
            :colour: str
        :infect_deck_discard: list of Card dicts
            :name: str
            :colour: str
        :diseases: dict of (colour => Disease dicts)
            :colour: str
            :cured: Boolean
            :public_health: int
        :cities: dict of (name => City dicts)
            :name: str
            :has_lab: Boolean
            :colour: str
            :infection_levels: dict (colour => lvl)
        :infection_rate: int
        :epidemic_count: int
        :active_character: str
        :skip_infect_phase: Boolean
        """
        characters = [cls.character_to_dict(character)
                      for character in game.characters]

        player_deck_discard = cls.deck_to_list(game.player_deck)
        infect_deck_discard = cls.deck_to_list(game.infect_deck)

        diseases = {colour: cls.disease_to_dict(disease)
                    for colour, disease in game.diseases.items()}
        cities = {name: cls.city_to_dict(city)
                  for name, city in game.city_map.items()}

        infection_rate = game.infection_rate
        epidemic_count = game.epidemic_count
        active_character = game.active_character
        skip_infect_phase = game.skip_infect_phase

        output = {
            'characters': characters,
            'player_deck_discard': player_deck_discard,
            'infect_deck_discard': infect_deck_discard,
            'diseases': diseases,
            'cities': cities,
            'infection_rate': infection_rate,
            'epidemic_count': epidemic_count,
            'active_character': active_character,
            'skip_infect_phase': skip_infect_phase
        }
        return output

    @classmethod
    def card_to_dict(cls, card):
        """
        :param card: Card object
        :return: New dict with Card properties
        :name: str
        :colour: str
        """
        output = {
            'name': card.name,
            'colour': card.colour,
        }
        return output

    @classmethod
    def deck_to_list(cls, deck):
        """
        :param deck: Deck object
        Does not return still uncovered cards
        :return: list of card dicts, card objects are copied
        """
        return [cls.card_to_dict(card) for card in deck.discard]

    @classmethod
    def city_to_dict(cls, city):
        """
        :param city: City object
        :return: Dict
        :name: str
        :has_lab: Boolean
        :colour: str
        :infection_levels: dict (colour => lvl)
        """
        output = {
            'name': city.name,
            'has_lab': city.has_lab,
            'colour': city.colour,
            'infection_levels': city.infection_levels.copy(),
        }
        return output

    @classmethod
    def disease_to_dict(cls, disease):
        """
        :param disease: Disease object
        :return: dict of properties
        :colour: str
        :cured: Boolean
        :public_health: int
        """
        output = {
            'colour': disease.colour,
            'cured': disease.cured,
            'public_health': disease.public_health,
        }
        return output

    @classmethod
    def character_to_dict(cls, character):
        """
        :param character: Character object
        :return: dict with character properties, nested objects are copied
        :name: str
        :location: str
        :action_count: int
        :hand: list of Card dicts
            :name: str
            :colour: str
        """
        output = {
            'name': character.name,
            'location': character.location.name,
            'action_count': character.action_count,
            'hand': [cls.card_to_dict(card) for card in character.hand],
        }
        return output
