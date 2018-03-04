from .abstractmrx import AbstractMrX


class AIDetective(AbstractMrX):
    def __init__(self, engine, num_players=4):
        super().__init__(engine, is_ai=True, num_players=num_players)

    def play_next(self):
        """TODO: insert AI logic here"""
        pass
