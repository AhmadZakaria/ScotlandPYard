from abc import ABC, abstractmethod


class AbstractPlayer(ABC):
    """This is the abstract player class that provides a basic interface for all players in the game."""

    def __init__(self, engine, is_ai=False):
        self.name = None
        self.tickets = None
        self.location = None
        self.is_ai = is_ai
        self.engine = engine

    @abstractmethod
    def play_next(self):
        """perform next action by player"""
        NotImplementedError("Class {} doesn't implement play_next()".format(self.__class__.__name__))

    @abstractmethod
    def get_role(self):
        NotImplementedError("Class {} doesn't implement get_role()".format(self.__class__.__name__))

    def set_location(self, location):
        self.location = location

    def get_info(self):
        """get player info"""
        stats = {
            "name": self.name,
            "is_ai": self.is_ai,
            "tickets": self.tickets,
            "location": self.location,
            "role": self.get_role()
        }
        return stats
