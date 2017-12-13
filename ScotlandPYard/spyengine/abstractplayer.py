from abc import ABC, abstractmethod


class AbstractPlayer(ABC):
    """This is the abstract player class that provides a basic interface for all players in the game."""

    def __init__(self, is_ai=False):
        self.name = None
        self.tickets = None
        self.is_ai=is_ai

    @abstractmethod
    def play_next(self):
        """perform next action by player"""
        NotImplementedError("Class {} doesn't implement play_next()".format(self.__class__.__name__))

    @abstractmethod
    def get_role(self):
        NotImplementedError("Class {} doesn't implement get_role()".format(self.__class__.__name__))

    def get_info(self):
        """get player info"""
        stats = {
            "name": self.name,
            "is_ai": self.is_ai,
            "tickets": self.tickets,
            "role": self.get_role()
        }
        return stats
