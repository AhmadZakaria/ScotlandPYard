import math

import networkx as nx
import pkg_resources
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .mapcomponents import Node, Edge
from .spyengine.maputils import get_map_graph


class SPYMap(QGraphicsView):
    def __init__(self, map_name):
        super(SPYMap, self).__init__()
        self.resourcepath = pkg_resources.resource_filename("ScotlandPYard.resources", "images")
        self.mapname = map_name + ".jpg"
        self.highlighted_nodes = []
        self.player_location = None

        self.timerId = 0
        scene = QGraphicsScene(self)
        scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.setScene(scene)

        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        # self.setRenderHint(QPainter.Antialiasing)
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
        # relabel the graph to make the Node instances themselves as the graph nodes.
        nx.relabel_nodes(self.graph, dict(nodes), copy=False)

        self.pos = nx.spring_layout(self.graph, scale=0.5, center=(0.5, 0.5), iterations=100)

        for n in self.graph.nodes():
            # node = Node(self, nodeid=n)
            n.setPos(*self.pos[n])
            self.scene().addItem(n)

        for e in self.graph.edges(data=True):
            src, dst, edgedata = e
            self.scene().addItem(Edge(src, dst, edgedata["ticket"]))

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

    def highlight_nodes(self, nodes=[]):
        for node in self.highlighted_nodes:
            node.set_highlight(False)
            node.update()

        for node in nodes:
            node.set_highlight(True)
            node.update()

        self.highlighted_nodes = nodes

    def set_player_turn(self, node):

        if self.player_location is not None:
            self.player_location.set_has_player(False)
        node.set_has_player(True)
        self.player_location = node

    # def redraw(self):
    #     self.clear()
    #     self.pixmap = self.pixmap_orig.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.FastTransformation)
    #     self.setSceneRect(self.pixmap.rect())
    #     self.scene().setSceneRect(self.pixmap.rect())
    #
    #     for edge in self.graph.edges():
    #         # print(edge)
    #         self.draw_edge(edge, brush=Qt.blue)
    #
    #     for edge in self.sub_graph.edges():
    #         # print(edge)
    #         self.draw_edge(edge, brush=Qt.yellow, stroke=1)
    #
    #     ellipse_side = 20
    #     for node in self.graph.nodes():
    #         self.draw_node(ellipse_side, node)
    #
    # def draw_edge(self, edge, brush=Qt.black, stroke=3):
    #     src, dst = edge
    #     src_pos = self.pos[src]
    #     dst_pos = self.pos[dst]
    #     self.addLine(src_pos[0] * self.pixmap.width(), src_pos[1] * self.pixmap.height(),
    #                  dst_pos[0] * self.pixmap.width(), dst_pos[1] * self.pixmap.height(), QPen(brush, stroke))
    #
    # def draw_node(self, ellipse_side, node):
    #     node_pos = self.pos[node]
    #     print(node_pos)
    #     half_side = ellipse_side / 2.0
    #     self.addEllipse(node_pos[0] * self.pixmap.width() - half_side, node_pos[1] * self.pixmap.height() - half_side,
    #                     ellipse_side, ellipse_side, brush=Qt.red)
