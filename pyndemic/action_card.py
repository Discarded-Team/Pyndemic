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


ACTION_CARDS = [
    GovernmentGrantActionCard
]
