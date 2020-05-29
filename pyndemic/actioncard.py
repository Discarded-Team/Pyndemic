from abc import ABC, abstractmethod


class ActionCard(ABC):
    """
    Action Cards can be played anytime, even during the other player's turn.
    Playing the card does not take any action points.
    """
    def __init__(self, ):
        self.name = None
        self.game = None

    @abstractmethod
    def check_payable(self, *args):
        pass

    @abstractmethod
    def play(self, *args):
        pass

    def __str__(self):
        return f'Action Card "{self.name}"'


class BuildLabActionCard(ActionCard):
    """
    Free of charge build a lab in any city.
    """
    def __init__(self):
        super().__init__()
        self.name = "Build Lab"

    def check_payable(self, city_name):
        if city_name not in self.game.city_map:
            return False
        return self.game.city_map[city_name].has_lab

    def play(self, city_name):
        if city_name not in self.game.city_map:
            return False
        self.game.city_map[city_name].build_lab()
        logging.info(
            f'Built a lab in {city_name}.')
        return True
