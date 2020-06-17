from abc import ABC, abstractmethod


class ActionCard(ABC):
    """
    Action Cards can be played anytime, even during the other player's turn.
    Playing the card does not take any action points.
    """
    def __init__(self, game):
        self.name = None
        self.game = game # the card changes the game, it needs a link

    @abstractmethod
    def check_payable(self, *args):
        pass

    @abstractmethod
    def play(self, *args):
        pass

    def __str__(self):
        return f'Action Card "{self.name}"'


class GovernmentGrantActionCard(ActionCard):
    """
    Build a lab in any city free of charge.
    """
    def __init__(self, game):
        super().__init__(game)
        self.name = "Government Grant"

    def check_payable(self, city_name):
        if city_name not in self.game.city_map:
            return False
        return self.game.city_map[city_name].has_lab

    def play(self, city_name):
        if city_name not in self.game.city_map:
            return False
        self.game.city_map[city_name].build_lab()
        logging.info(
            f'Action: Built a lab in {city_name}.')
        return True


ACTION_CARDS = [
    GovernmentGrantActionCard
]
