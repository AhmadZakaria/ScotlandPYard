#!/usr/bin/env python

#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################

import math

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Edge(QGraphicsItem):
    Pi = math.pi
    TwoPi = 2.0 * Pi

    Type = QGraphicsItem.UserType + 2

    def __init__(self, sourceNode, destNode, ticket="Taxi"):
        super(Edge, self).__init__()

        self.arrowSize = 10.0
        self.sourcePoint = QPointF()
        self.destPoint = QPointF()
        self.ticket = ticket

        self.setAcceptedMouseButtons(Qt.NoButton)
        self.source = sourceNode
        self.dest = destNode
        self.source.addEdge(self)
        self.dest.addEdge(self)
        self.adjust()
        self.setZValue(2)

        self.brush = {"Taxi": Qt.white, "Underground": Qt.red, "Bus": Qt.blue}

    def type(self):
        return Edge.Type

    def sourceNode(self):
        return self.source

    def setSourceNode(self, node):
        self.source = node
        self.adjust()

    def destNode(self):
        return self.dest

    def setDestNode(self, node):
        self.dest = node
        self.adjust()

    def adjust(self):
        if not self.source or not self.dest:
            return

        line = QLineF(self.mapFromItem(self.source, 0, 0),
                      self.mapFromItem(self.dest, 0, 0))
        length = line.length()

        self.prepareGeometryChange()

        if length > 20.0:
            edgeOffset = QPointF((line.dx() * 10) / length,
                                 (line.dy() * 10) / length)

            self.sourcePoint = line.p1() + edgeOffset
            self.destPoint = line.p2() - edgeOffset
        else:
            self.sourcePoint = line.p1()
            self.destPoint = line.p1()

    def boundingRect(self):
        if not self.source or not self.dest:
            return QRectF()

        penWidth = 1.0
        extra = (penWidth + self.arrowSize) / 2.0

        return QRectF(self.sourcePoint,
                      QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                             self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra, -extra, extra,
                                                                                               extra)

    def paint(self, painter, option, widget):
        if not self.source or not self.dest:
            return

        # Draw the line itself.
        line = QLineF(self.sourcePoint, self.destPoint)

        if line.length() == 0.0:
            return

        painter.setPen(QPen(self.brush[self.ticket], 1, Qt.SolidLine, Qt.RoundCap,
                            Qt.RoundJoin))
        painter.drawLine(line)

        # # Draw the arrows if there's enough room.
        # angle = math.acos(line.dx() / line.length())
        # if line.dy() >= 0:
        #     angle = Edge.TwoPi - angle

        # sourceArrowP1 = self.sourcePoint + QPointF(math.sin(angle + Edge.Pi / 3) * self.arrowSize,
        #                                            math.cos(angle + Edge.Pi / 3) * self.arrowSize)
        # sourceArrowP2 = self.sourcePoint + QPointF(math.sin(angle + Edge.Pi - Edge.Pi / 3) * self.arrowSize,
        #                                            math.cos(angle + Edge.Pi - Edge.Pi / 3) * self.arrowSize)
        # destArrowP1 = self.destPoint + QPointF(math.sin(angle - Edge.Pi / 3) * self.arrowSize,
        #                                        math.cos(angle - Edge.Pi / 3) * self.arrowSize)
        # destArrowP2 = self.destPoint + QPointF(math.sin(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize,
        #                                        math.cos(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize)

        # painter.setBrush(Qt.black)
        # painter.drawPolygon(QPolygonF([line.p1(), sourceArrowP1, sourceArrowP2]))
        # painter.drawPolygon(QPolygonF([line.p2(), destArrowP1, destArrowP2]))


class Node(QGraphicsItem):
    Type = QGraphicsItem.UserType + 1

    def __init__(self, graphWidget, nodeid=""):
        super(Node, self).__init__()

        self.graph = graphWidget
        self.edgeList = []
        self.newPos = QPointF()
        self.nodeid = str(nodeid)
        self.highlight = False
        self.has_player = False
        self.has_turn_player = False

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(2)

        # initialize available means to correctly color the node
        self.available_means = {"Taxi": False, "Underground": False, "Bus": False}

    def type(self):
        return Node.Type

    def addEdge(self, edge):
        self.available_means[edge.ticket] = True
        self.edgeList.append(edge)
        edge.adjust()

    def edges(self):
        return self.edgeList

    def calculateForces(self):
        if not self.scene() or self.scene().mouseGrabberItem() is self:
            self.newPos = self.pos()
            return

        # Sum up all forces pushing this item away.
        xvel = 0.0
        yvel = 0.0
        for item in self.scene().items():
            if not isinstance(item, Node):
                continue

            line = QLineF(self.mapFromItem(item, 0, 0), QPointF(0, 0))
            dx = line.dx()
            dy = line.dy()
            l = 2.0 * (dx * dx + dy * dy)
            if l > 0:
                xvel += (dx * 150.0) / l
                yvel += (dy * 150.0) / l

        # Now subtract all forces pulling items together.
        weight = (len(self.edgeList) + 1) * 1.5
        for edge in self.edgeList:
            if edge.sourceNode() is self:
                pos = self.mapFromItem(edge.destNode(), 0, 0)
            else:
                pos = self.mapFromItem(edge.sourceNode(), 0, 0)
            xvel += pos.x() / weight
            yvel += pos.y() / weight

        if qAbs(xvel) < 0.1 and qAbs(yvel) < 0.1:
            xvel = yvel = 0.0

        sceneRect = self.scene().sceneRect()
        self.newPos = self.pos() + QPointF(xvel, yvel)
        self.newPos.setX(min(max(self.newPos.x(), sceneRect.left() + 10), sceneRect.right() - 10))
        self.newPos.setY(min(max(self.newPos.y(), sceneRect.top() + 10), sceneRect.bottom() - 10))

    def set_highlight(self, hl):
        self.highlight = hl

    def set_has_player(self, hasplayer):
        self.has_player = hasplayer

    def set_has_turn_player(self, hasturnplayer):
        self.has_turn_player = hasturnplayer

    def advance(self):
        if self.newPos == self.pos():
            return False

        self.setPos(self.newPos)
        return True

    def boundingRect(self):
        adjust = 2.0
        return QRectF(-15 - adjust / 2, -15 - adjust / 2, 30 + adjust, 30 + adjust)

    def shape(self):
        path = QPainterPath()
        path.addEllipse(self.boundingRect())
        return path

    def paint(self, painter, option, widget):
        bus_clr = Qt.blue if self.available_means["Bus"] else Qt.white
        underground_clr = Qt.red if self.available_means["Underground"] else Qt.white

        gradient = QLinearGradient()
        if option.state & QStyle.State_Sunken:
            gradient.setColorAt(1, QColor(bus_clr).lighter(120))
            gradient.setColorAt(0, QColor(underground_clr).lighter(120))
        else:
            gradient.setColorAt(0, bus_clr)
            gradient.setColorAt(0.5, underground_clr)

        if self.highlight:
            painter.setBrush(Qt.green)
            painter.setPen(QPen(Qt.green, 1))
            painter.drawEllipse(-15, -15, 30, 30)

        if self.has_player:
            painter.setBrush(Qt.magenta)
            painter.setPen(QPen(Qt.magenta, 1))
            painter.drawEllipse(-15, -15, 30, 30)

        if self.has_turn_player:
            painter.setBrush(Qt.cyan)
            painter.setPen(QPen(Qt.cyan, 1))
            painter.drawEllipse(-15, -15, 30, 30)

        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(Qt.black, 0))
        painter.drawEllipse(-10, -10, 20, 20)
        painter.fillRect(-5, -5, 10, 10, Qt.white)

        font = painter.font()
        font.setBold(True)
        font.setPointSize(7)
        painter.setFont(font)
        painter.setPen(Qt.black)
        painter.drawText(-5, 5, self.nodeid)

    def itemChange(self, change, value):
        # if change == QGraphicsItem.ItemPositionHasChanged:
        for edge in self.edgeList:
            edge.adjust()
        self.graph.itemMoved()

        return super(Node, self).itemChange(change, value)

    def mouseDoubleClickEvent(self, event):
        self.graph.handleNodeClick(self)
        self.update()
        super(Node, self).mouseReleaseEvent(event)

    def mousePressEvent(self, event):
        self.update()
        super(Node, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        super(Node, self).mouseReleaseEvent(event)

    def __str__(self):
        return "Node:({})".format(self.nodeid)

    def __repr__(self):
        return "Node:({})".format(self.nodeid)
