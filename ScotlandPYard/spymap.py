import math

import networkx as nx
import pkg_resources
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from .mapcomponents import Node, Edge
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

        self.timerId = 0
        scene = QGraphicsScene(self)
        scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.setScene(scene)

        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)

        # self.pixmap_orig = QPixmap(os.path.join(self.resourcepath, map_name))
        # self.pixmap = self.pixmap_orig.scaled(self.pixmap_orig.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # self.pixmap_item = self.scene().addPixmap(self.pixmap)

        self.init_graph(map_name)

    def init_graph(self, map_name):
        # get saved map graph
        self.graph = get_map_graph(map_name)
        # map node numbers to visual Node instances
        nodes = [[i, Node(self, nodeid=i)] for i in self.graph.nodes()]
        node_dict = dict(nodes)
        # relabel the graph to make the Node instances themselves as the graph nodes.
        nx.relabel_nodes(self.graph, node_dict, copy=False)

        self.pos = nx.spring_layout(self.graph, scale=250, center=(0, 0), iterations=100)

        for e in self.graph.edges(data=True):
            src, dst, edgedata = e
            self.scene().addItem(Edge(src, dst, edgedata['path'], node_dict, edgedata["ticket"]))

        for n in self.graph.nodes():
            # node = Node(self, nodeid=n)
            n.setPos(*self.pos[n])
            self.scene().addItem(n)

    def resizeEvent(self, event):
        # self.scene().removeItem(self.pixmap_item)
        # self.pixmap = self.pixmap_orig.scaled(event.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # self.pixmap_item = self.scene().addPixmap(self.pixmap)
        # self.scene().setSceneRect(QRectF(self.pixmap.rect()))

        for n in self.graph.nodes():
            # x, y = self.pos[n]
            n.setPos(*self.pos[n])
            # n.setPos(x * self.pixmap.width(), y * self.pixmap.height())

        self.scene().update()

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
        nodes = [item for item in self.scene().items() if isinstance(item, Node)]

        for node in nodes:
            node.calculateForces()

        itemsMoved = False
        for node in nodes:
            if node.advance():
                self.pos[node] = [node.pos().x(), node.pos().y()]
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
        for node in self.players_locations:
            node.set_has_player(False)
            node.update()

        for node in locs:
            node.set_has_player(True)
            node.update()

        self.players_locations = locs

    def setEngine(self, engine):
        self.engine = engine

    def handleNodeClick(self, node):
        # print("handleNodeClick from", node.nodeid)
        if node in self.highlighted_nodes:
            self.engine.sendNextMove(node, self.last_ticket)
