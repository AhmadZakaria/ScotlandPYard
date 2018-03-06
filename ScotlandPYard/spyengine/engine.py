from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from numpy.random import choice

from .StupidAIDetective import StupidAIDetective
from .humandetective import HumanDetective
from .humanmrx import HumanMrX


class IllegalMoveException(Exception):
    pass


class GameEngine(QObject):
    game_state_changed = pyqtSignal()

    def __init__(self, spymap, num_detectives=4):
        super(GameEngine, self).__init__()
        self.spymap = spymap
        self.graph = spymap.graph
        self.num_detectives = num_detectives
        # self.players = [HumanDetective(self) for i in range(num_detectives)]
        self.players = [HumanDetective(self), StupidAIDetective(self), StupidAIDetective(self), StupidAIDetective(self)]
        self.turn = 0
        taken_locations = set()
        for detective in self.players:
            chosen = choice(list(set(self.graph.nodes()).difference(taken_locations)))
            taken_locations.add(chosen)
            detective.set_location(chosen)

        self.mrx = HumanMrX(self, num_players=num_detectives)
        self.mrx.set_location(choice(list(set(self.graph.nodes()).difference(taken_locations))))
        self.players.append(self.mrx)

    def get_game_state(self):
        state = {
            "players_state": [player.get_info() for player in self.players],
            "turn": self.turn
        }
        return state

    def get_valid_nodes(self, player_name, ticket):
        player = None
        for p in self.players:
            if p.name == player_name:
                player = p
                break
        if player is None: return []

        valid_nodes = []
        for u, v, tick in self.graph.edges(nbunch=player.location, data='ticket'):
            if tick == ticket and player.tickets[ticket] > 0:
                valid_nodes.append(v)

        # print("Player now at: {}".format(player.location.nodeid))
        # print("Available moves by {}: ".format(ticket))
        # print([n.nodeid for n in valid_nodes])

        return valid_nodes

    def sendNextMove(self, node, ticket):
        player = self.players[self.turn]
        if node not in self.get_valid_nodes(player.name, ticket):
            raise IllegalMoveException("This move is not allowed.")

        player.tickets[ticket] -= 1
        player.set_location(node)
        self.turn = (self.turn + 1) % len(self.players)

        self.game_state_changed.emit()

        # prompt next player to play if its AI.
        if self.players[self.turn].is_ai:
            # print("is AI")
            # Wait for 1 second to simulate thinking and give people time to see
            QTimer.singleShot(1000, lambda: self.players[self.turn].play_next())
