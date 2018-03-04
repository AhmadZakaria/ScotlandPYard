from .abstractdetective import AbstractDetective


class AIDetective(AbstractDetective):
    def __init__(self, engine, name=None):
        super().__init__(engine, is_ai=True, name=name)

    def play_next(self):
        """TODO: insert AI logic here"""
        pass
