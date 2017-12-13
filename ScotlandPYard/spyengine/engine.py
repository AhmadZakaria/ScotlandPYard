from PyQt5.QtCore import *

from .humandetective import HumanDetective
from .humanmrx import HumanMrX


class Game(QThread):
    def __init__(self, num_detectives=4):
        self.detectives = []
        # to be set to true whenever a player makes a move each round
        self.turns = [False for i in range(num_detectives+1)]
        for i in range(num_detectives):
            detective = HumanDetective()
            self.detectives.append(detective)

        self.mrx = HumanMrX(num_players=num_detectives)

    def get_game_state(self):
        state = {
            "detectives": [detective.get_info() for detective in self.detectives],
            "Mr. X": self.mrx.get_info()
        }
        return state

    # def run(self):
        
