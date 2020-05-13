

class BaseFormatter:
    '''
    Provides methods of serialisation of Game instance for various viewpoints
    '''

    @classmethod
    def game_to_dict(cls, game):
        """
        :param game: Game object
        :return: dict with (almost) complete state of the game. Decks return
            only the discard.
        :players: list of Player dicts
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
        """
        output = {}
        output['players'] = \
            [cls.player_to_dict(player) for player in game.players]
        output['player_deck_discard'] = cls.deck_to_list(game.player_deck)
        output['infect_deck_discard'] = cls.deck_to_list(game.infect_deck)
        output['diseases'] = {colour: cls.disease_to_dict(disease)
                              for colour, disease in game.diseases.items()}
        output['cities'] = {name: cls.city_to_dict(city)
                            for name, city in game.city_map.items()}
        output['infection_rate'] = game.infection_rate
        output['epidemic_count'] = game.epidemic_count

        return output

    @classmethod
    def card_to_dict(cls, card):
        """
        :param card: Card object
        :return: New dict with Card properties
        :name: str
        :colour: str
        """
        return {'name': card.name, 'colour': card.colour}

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
        output = {}
        output['name'] = city.name
        output['has_lab'] = city.has_lab
        output['colour'] = city.colour
        output['infection_levels'] = city.infection_levels.copy()
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
        output = {}
        output['colour'] = disease.colour
        output['cured'] = disease.cured
        output['public_health'] = disease.public_health
        return output

    @classmethod
    def player_to_dict(cls, player):
        """
        :param player: Player object
        :return: dict with player properties, nested objects are copied
        :name: str
        :location: str
        :action_count: int
        :hand: list of Card dicts
            :name: str
            :colour: str
        """
        output = {}
        output['name'] = player.name
        output['location'] = player.location.name
        output['action_count'] = player.action_count
        output['hand'] = [cls.card_to_dict(card) for card in player.hand]
        return output
