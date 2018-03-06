import networkx as nx
from ScotlandPYard.config.gameconfig import maps


def get_map_graph(map_name):
    if map_name not in maps:
        raise NotImplementedError("This map is not implemented yet: {}".format(map_name))

    map = maps[map_name]
    G = nx.MultiGraph()
    for ticket in map["connections"]:
        for path in map["connections"][ticket]:
            G.add_edge(path[0], path[-1], ticket=ticket, path=path)

    return G
