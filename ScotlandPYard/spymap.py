import math
import os

import networkx as nx
import pkg_resources
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from numpy.random import choice

from .mapcomponents import Node, Edge


class SPYMap(QGraphicsView):
    def __init__(self):
        super(SPYMap, self).__init__()
        self.resourcepath = pkg_resources.resource_filename("ScotlandPYard.resources", "images")

        self.timerId = 0
        scene = QGraphicsScene(self)
        scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.setScene(scene)

        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        # self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)

        self.pixmap_orig = QPixmap(os.path.join(self.resourcepath, 'map3_.jpg'))
        self.pixmap = self.pixmap_orig.scaled(self.pixmap_orig.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.pixmap_item = self.scene().addPixmap(self.pixmap)

        self.init_graph()

    def init_graph(self):
        # dummy graph
        nodes = [Node(self, nodeid=i) for i in range(100)]
        self.graph = nx.gnm_random_graph(len(nodes), 150)
        nx.relabel_nodes(self.graph, dict(enumerate(nodes)), copy=False)  # if copy = True then it returns a copy.

        randnode = choice(self.graph.nodes())
        self.sub_graph = nx.ego_graph(self.graph, randnode)

        for e in self.graph.edges(data=True):
            edgedata = e[2]
            edgedata["type"] = choice(["Taxi", "Underground", "Bus"])
        # end dummy graph

        self.pos = nx.spring_layout(self.graph, scale=0.5, center=(0.5, 0.5), iterations=100)

        for n in self.graph.nodes():
            # node = Node(self, nodeid=n)
            n.setPos(*self.pos[n])
            self.scene().addItem(n)

        for e in self.graph.edges(data=True):
            src, dst, edgedata = e
            self.scene().addItem(Edge(src, dst, edgedata["type"]))

    def resizeEvent(self, event):
        self.scene().removeItem(self.pixmap_item)
        self.pixmap = self.pixmap_orig.scaled(event.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.pixmap_item = self.scene().addPixmap(self.pixmap)
        self.scene().setSceneRect(QRectF(self.pixmap.rect()))

        for n in self.graph.nodes():
            x, y = self.pos[n]
            n.setPos(x * self.pixmap.width(), y * self.pixmap.height())

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
                itemsMoved = True

        if not itemsMoved:
            self.killTimer(self.timerId)
            self.timerId = 0
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
