import math

import networkx as nx
import numpy as np
import pkg_resources
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .mapcomponents import Node, Edge
from .profile_utils import print_prof_data, profile
from .spyengine.maputils import get_map_graph


class SPYMap(QGraphicsView):
    def __init__(self, map_name):
        super(SPYMap, self).__init__()
        self.resourcepath = pkg_resources.resource_filename("ScotlandPYard.resources", "images")
        self.mapname = map_name + ".jpg"
        self.highlighted_nodes = []
        self.turn_player_location = None
        self.players_locations = []
        self.engine = None
        self.last_ticket = None
        self.icons = []

        self.timerId = 0
        scene = QGraphicsScene(self)
        scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.setScene(scene)

        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)

        self.init_graph(map_name)

    def init_graph(self, map_name):
        # get saved map graph
        self.graph = get_map_graph(map_name)
        # map node numbers to visual Node instances
        nodes = [[i, Node(self, nodeid=i)] for i in self.graph.nodes()]
        node_dict = dict(nodes)
        # relabel the graph to make the Node instances themselves as the graph nodes.
        nx.relabel_nodes(self.graph, node_dict, copy=False)

        # self.pos = nx.spring_layout(self.graph, scale=250, center=(0, 0), iterations=100)
        print("Setting up graph..")
        self.pos = nx.spring_layout(self.graph, scale=600, center=(0, 0), iterations=50)

        for e in self.graph.edges(data=True):
            src, dst, edgedata = e
            self.scene().addItem(Edge(src, dst, edgedata['path'], node_dict, edgedata["ticket"]))

        for n in self.graph.nodes():
            n.setPos(*self.pos[n])
            self.scene().addItem(n)

    # def resizeEvent(self, event: QResizeEvent):
    # print("Resize")
    # self.fitInView(self.scene().itemsBoundingRect(), Qt.KeepAspectRatioByExpanding)

    def wheelEvent(self, event):
        self.scaleView(math.pow(2.0, -event.angleDelta().y() / 240.0))

    def scaleView(self, scaleFactor):
        factor = self.transform().scale(scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        self.scale(scaleFactor, scaleFactor)

    def itemMoved(self):
        if not self.timerId:
            self.timerId = self.startTimer(1000 / 25)

    def timerEvent(self, event):
        self.update_nodes()
        print_prof_data()

    @profile
    def update_nodes(self):
        pos_mat = np.array([[-item.pos().x(), -item.pos().y()] for item in self.graph.nodes()])

        for node in self.graph.nodes():
            node.calculateForces(pos_mat)

        itemsMoved = False
        for node in self.graph.nodes():
            if node.advance():
                itemsMoved = True
        if not itemsMoved:
            self.killTimer(self.timerId)
            self.timerId = 0

    def unhighlight_nodes(self):
        for node in self.highlighted_nodes:
            node.set_highlight(False)
            node.update()

    def highlight_nodes(self, nodes=[], ticket="Taxi"):
        self.unhighlight_nodes()

        for node in nodes:
            node.set_highlight(True)
            node.update()

        self.highlighted_nodes = nodes
        self.last_ticket = ticket

    def update_state(self):
        loc = self.engine.players[self.engine.turn].location
        self.set_player_turn(loc)

        self.set_player_locations([(p.name, p.location) for p in self.engine.players[:-1]])

    def set_player_turn(self, node):
        self.unhighlight_nodes()
        if self.turn_player_location is not None:
            self.turn_player_location.set_has_turn_player(False)
            self.turn_player_location.update()
        node.set_has_turn_player(True)
        node.update()
        self.turn_player_location = node

    def set_player_locations(self, locs):
        self.unhighlight_nodes()
        for name, node in self.players_locations:
            node.set_has_player(False)
            node.update()

        margin = 35
        for name, node in locs:
            node.set_has_player(True)
            node.update()
            self.icons[name].setPos(node.pos().x() - margin,
                                    node.pos().y() - margin)

        self.players_locations = locs

    def setEngine(self, engine):
        self.engine = engine
        self.icons = dict([[p.name, p.icon] for p in engine.players[:-1]])
        for name, icon in self.icons.items():
            self.scene().addItem(icon)

    def handleNodeClick(self, node):
        # print("handleNodeClick from", node.nodeid)
        if node in self.highlighted_nodes:
            self.engine.sendNextMove(node, self.last_ticket)
