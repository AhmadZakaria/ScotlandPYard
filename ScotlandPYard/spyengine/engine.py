from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from numpy.random import choice

from .StupidAIDetective import StupidAIDetective
from .StupidAIMrX import StupidAIMrX
from .abstractdetective import AbstractDetective
from .abstractmrx import AbstractMrX


class IllegalMoveException(Exception):
    pass


class GameEngine(QObject):
    game_state_changed = pyqtSignal()
    game_over_signal = pyqtSignal(str)

    def __init__(self, spymap, num_detectives=4, maxMoves=30, revealedstates=[]):
        super(GameEngine, self).__init__()
        self.spymap = spymap
        self.graph = spymap.graph
        self.num_detectives = num_detectives
        self.maxMoves = maxMoves
        self.revealedstates = revealedstates
        # self.players = [HumanDetective(self) for i in range(num_detectives)]
        self.players = [StupidAIDetective(self), StupidAIDetective(self), StupidAIDetective(self)]
        self.turn = 0
        self.game_over = False
        self.mrxMoves = []
        self.mrxLastKnownLocation = None
        taken_locations = set()
        for detective in self.players:
            chosen = choice(list(set(self.graph.nodes()).difference(taken_locations)))
            taken_locations.add(chosen)
            detective.set_location(chosen)

        self.mrx = StupidAIMrX(self, num_players=num_detectives)
        self.mrx.set_location(choice(list(set(self.graph.nodes()).difference(taken_locations))))
        self.players.append(self.mrx)
        self.game_state_changed.connect(self.check_game_state)

    def get_game_state(self):
        state = {
            "players_state": [player.get_info() for player in self.players],
            "turn": self.turn,
            "mrxmoves": self.mrxMoves
        }
        return state

    def check_game_state(self):
        '''
        Checks if the game is over or not
        '''
        for p in self.players[:-1]:
            if p.location == self.mrx.location:
                self.game_over = True
                msg = "{} has caught Mr.X\n\tGame over!".format(p.name)

        if len(self.mrxMoves) == self.maxMoves:
            self.game_over = True
            msg = "Mr.X has evaded justice!\n\tGame over!"

        if self.game_over:
            self.game_over_signal.emit(msg)
            print(msg)

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

    def sendNextMove(self, node=None, ticket="Taxi"):
        if node is not None:
            player = self.players[self.turn]
            if node not in self.get_valid_nodes(player.name, ticket):
                raise IllegalMoveException("This move is not allowed.")

            player.tickets[ticket] -= 1
            if isinstance(player, AbstractDetective):
                self.mrx.tickets[ticket] += 1

            if isinstance(player, AbstractMrX):
                if len(self.mrxMoves) in self.revealedstates:
                    self.mrxLastKnownLocation = node.nodeid
                    self.mrxMoves.append([self.mrxLastKnownLocation, ticket])
                else:
                    self.mrxMoves.append([None, ticket])

            player.set_location(node)

        self.turn = (self.turn + 1) % len(self.players)
        self.game_state_changed.emit()

        # prompt next player to play if its AI.
        if self.players[self.turn].is_ai and not self.game_over:
            # print("is AI")
            # Wait for 1 second to simulate thinking and give people time to see
            QTimer.singleShot(50, lambda: self.players[self.turn].play_next())

    def start_game(self):
        self.players[self.turn].play_next()
