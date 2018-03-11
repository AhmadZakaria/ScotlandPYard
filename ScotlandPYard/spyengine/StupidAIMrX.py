from numpy.random import choice

from .aimrx import AIMrX


class StupidAIMrX(AIMrX):
    def play_next(self):
        moves = []
        for t in self.tickets.keys():
            if self.tickets[t] > 0:
                moves.extend([(n, t) for n in self.engine.get_valid_nodes(self.name, t)])

        # print("Stupid AI: mesa thinks one of those is good")
        if len(moves) > 0:
            idx = choice(len(moves))
            random_move = moves[idx]
            node, ticket = random_move
            # print("Stupid AI: mesa choose to go to {} with dis {} yaaa".format(node.nodeid, ticket))
        else:
            node = None
            ticket = None
        self.engine.sendNextMove(node, ticket)
