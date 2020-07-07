from .core import GameEntity


# TODO: add more test cases for this module
class Card(GameEntity):
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

    def __str__(self):
        return f'Card "{self.name}-{self.colour}"'

    def on_draw(self, character_drawing):
        pass

    def on_play(self, character_playing):
        pass

    def on_discard(self, character_discarding):
        pass


class PlayerCard(Card):
    def on_draw(self, character_drawing):
        character_drawing.add_card(self)
        self.emit_signal(
            f'{character_drawing} drew {self}.',
        )


class CityCard(PlayerCard):
    pass


class EpidemicCard(PlayerCard):
    def __init__(self):
        self.name = 'Epidemic'
        self.colour = None

    def on_draw(self, character_drawing):
        super().on_draw(character_drawing)

        self.emit_signal(
            f'{character_drawing} drew Epidemic!',
        )

        self.game = self._ctx['controller']().game
        self.game.epidemic_phase()


class ActionCard(PlayerCard):
    def __init__(self, name):
        self.name = name
        self.colour = None


class InfectCard(Card):
    def on_draw(self, character_drawing):
        super().on_draw(character_drawing)

        self.game = self._ctx['controller']().game
        city = self.game.city_map[self.name]
        self.game.infect_city(self.name, self.colour)
