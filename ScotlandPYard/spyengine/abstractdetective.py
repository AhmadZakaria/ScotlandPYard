import petname

from .abstractplayer import AbstractPlayer


class AbstractDetective(AbstractPlayer):
    def __init__(self, name=None):
        super().__init__()

        if name is None:
            # generate random animal name
            name = petname.generate(words=2, letters=10, separator=" ")

        self.name = name
        self.tickets = {
            "Bus": 8,
            "Taxi": 10,
            "Underground": 4
        }
