import petname

from .abstractplayer import AbstractPlayer


class AbstractDetective(AbstractPlayer):
    def __init__(self, engine, is_ai=False, name=None):
        super().__init__(engine, is_ai=is_ai)

        if name is None:
            # generate random animal name
            name = petname.generate(words=2, letters=10, separator=" ")

        self.name = name
        self.tickets = {
            "Bus": 8,
            "Taxi": 10,
            "Underground": 4
        }

    def get_role(self):
        return "detective"
