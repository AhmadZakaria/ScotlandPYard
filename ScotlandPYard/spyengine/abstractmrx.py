import petname

from .abstractplayer import AbstractPlayer


class AbstractMrX(AbstractPlayer):
    def __init__(self, num_players=4):
        super().__init__()

        self.name = "Mr. X"
        self.tickets = {
            "Bus": 3,
            "Taxi": 4,
            "Underground": 3,
            "2x": 2,
            "BlackTicket": num_players
        }
