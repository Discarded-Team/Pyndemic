from .card import ActionCard


class GovernmentGrantActionCard(ActionCard):
    """
    Build a lab in any city free of charge.
    """

    def __init__(self):
        super().__init__()
        self.name = "Government Grant"

    def check_payable(self, city_name):
        game = self._ctx['controller']().game
        if city_name not in game.city_map:
            return False
        return not game.city_map[city_name].has_lab

    def on_play(self, city_name):
        game = self._ctx['controller']().game
        if self.check_payable(city_name):
            game.city_map[city_name].build_lab()
            self.emit_signal(
                f'Action: Built a lab in {city_name}.',
            )
            return True
        else:
            return False


class QuietNightActionCard(ActionCard):
    """
    Next player turn does not have infection phase.
    The current player infection phase is still active though.

    game.infect_phase_mode cycles through:
    'normal'->'skip for the next player' by Card
    'skip for the next player'->'skip for the current player' by Controller
    'skip for the current player'->'normal' by Game
    """

    def __init__(self):
        super().__init__()
        self.name = "Quiet Night"

    def check_payable(self):
        return True

    def on_play(self):
        game = self._ctx['controller']().game
        game.infect_phase_mode = "skip for the next player"


# repeats are in order to take physical space in the deck
ACTION_CARDS = [
    GovernmentGrantActionCard,
    QuietNightActionCard,
    GovernmentGrantActionCard,
    GovernmentGrantActionCard,
    GovernmentGrantActionCard
]
