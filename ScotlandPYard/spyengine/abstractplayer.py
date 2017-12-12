from abc import ABC, abstractmethod


class AbstractPlayer(ABC):
    """This is the abstract player class that provides a basic interface for all players in the game."""

    def __init__(self):
        self.name = None
        self.tickets = None

    @abstractmethod
    def play_next(self):
        NotImplementedError("Class {} doesn't implement play_next()".format(self.__class__.__name__))
