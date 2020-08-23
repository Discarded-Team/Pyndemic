from .card import ActionCard


class GovernmentGrantActionCard(ActionCard):
    """
    Build a lab in any city free of charge.
    """

    def __init__(self):
        super().__init__()
        self.name = "Government Grant"

    def check_playable(self, city_name):
        game = self._ctx['controller']().game
        if city_name not in game.city_map:
            return False
        return not game.city_map[city_name].has_lab

    def on_play(self, city_name):
        game = self._ctx['controller']().game
        if self.check_playable(city_name):
            game.city_map[city_name].build_lab()
            self.emit_signal(
                f'Action: Built a lab in {city_name}.',
            )
            return True
        else:
            return False


class OneQuietNightActionCard(ActionCard):
    """
    The next infection phase is skipped.
    """

    def __init__(self):
        super().__init__()
        self.name = "One Quiet Night"

    def check_playable(self):
        return True

    def on_play(self):
        game = self._ctx['controller']().game
        game.skip_infect_phase = True


# repeats are in order to take physical space in the deck
ACTION_CARDS = [
    GovernmentGrantActionCard,
    OneQuietNightActionCard,
    GovernmentGrantActionCard,
    GovernmentGrantActionCard,
    GovernmentGrantActionCard
]
