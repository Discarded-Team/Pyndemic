from .core import GameEntity


class Card(GameEntity):
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

    def __str__(self):
        return f'Card "{self.name}-{self.colour}"'

    def on_draw(self, *args, **kwargs):
        pass

    def on_play(self, *args, **kwargs):
        pass

    def on_discard(self, *args, **kwargs):
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
        self.emit_signal(
            f'{character_drawing} drew Epidemic!',
        )

        game = self._ctx['controller']().game
        game.epidemic_phase()


class ActionCard(PlayerCard):
    """
    Action Cards can be played anytime, even during the other player's turn.
    Playing the card does not take any action points.
    """

    def __init__(self):
        self.name = None
        self.colour = None

    def check_playable(self, *args):
        pass

    def __str__(self):
        return f'Action Card "{self.name}"'


class InfectCard(Card):
    def on_draw(self, character_drawing):
        self.on_play(character_drawing)

    def on_play(self, character_playing):
        game = self._ctx['controller']().game
        game.infect_city(self.name, self.colour)
        game.outbreak_stack.clear()
        game.infect_deck.add_discard(self)
