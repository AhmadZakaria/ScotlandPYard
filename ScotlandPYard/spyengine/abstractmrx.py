from .abstractplayer import AbstractPlayer


class AbstractMrX(AbstractPlayer):
    def __init__(self, engine, is_ai=False, num_players=4):
        super().__init__(engine, is_ai=is_ai)

        self.name = "Mr. X"
        self.tickets = {
            "Bus": 3,
            "Taxi": 4,
            "Underground": 3,
            "2x": 2,
            "BlackTicket": num_players
        }

    def get_role(self):
        return "Mr. X"
