from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import networkx as nx

class PrettyWidget(QWidget):

    NumButtons = ['btn'+str(i) for i in range(1,32)]

    def __init__(self):


        super(PrettyWidget, self).__init__()        
        font = QFont()
        font.setPointSize(16)
        self.initUI()

    def initUI(self):

        self.setGeometry(100, 100, 800, 800)
        self.center()
        self.setWindowTitle('S. pyard')

        mainLayout = QHBoxLayout()
        self.setLayout(mainLayout)
        
        self.createThiefMovesGroupBox() 
        self.createPlayersDashHBox() 

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)    
        
        self.createLeftBox()
        
        mainLayout.addWidget(self.leftBox,1 )
        mainLayout.addWidget(self.thiefMovesGroupBox)
        
        self.showMap()
        
        self.show()


    def createThiefMovesGroupBox(self):
        self.thiefMovesGroupBox = QGroupBox()

        layout = QVBoxLayout()
        for i in  self.NumButtons:
            button = QPushButton(i)
            button.setObjectName(i)
            layout.addWidget(button)
            self.thiefMovesGroupBox.setLayout(layout)
#            button.clicked.connect(self.submitCommand)

    def createPlayersDashHBox(self):
        self.playersDashHBox = QGroupBox()
        
        layout = QHBoxLayout()
        for i in range (1,6):
            playerDash = self.getNewPlayerDash("Player "+str(i))
            layout.addWidget(playerDash)
            self.playersDashHBox.setLayout(layout)
            
        
    def getNewPlayerDash(self, playerName):
        items = {'Taxi':10, 'Bus':8, 'Underground':5}
        playerDash = QGroupBox()
        
        layout = QVBoxLayout()
        for k, v in  items.items():
            button = QPushButton("{} x{}".format(k,v))
            button.setObjectName(k)
            layout.addWidget(button)
            playerDash.setLayout(layout)
        return playerDash
        
    def createLeftBox(self):
        self.leftBox = QGroupBox()
        layout = QVBoxLayout()
        layout.addWidget(self.canvas, 1)
        layout.addWidget(self.playersDashHBox)
        self.leftBox.setLayout(layout)
        
    def showMap(self):
        self.figure.clf()
        B = nx.Graph()
        B.add_nodes_from([1, 2, 3, 4], bipartite=0)
        B.add_nodes_from(['a', 'b', 'c', 'd', 'e'], bipartite=1)
        B.add_edges_from([(1, 'a'), (2, 'c'), (3, 'd'), (3, 'e'), (4, 'e'), (4, 'd')])

        X = set(n for n, d in B.nodes(data=True) if d['bipartite'] == 0)
        Y = set(B) - X

        X = sorted(X, reverse=True)
        Y = sorted(Y, reverse=True)

        pos = dict()
        pos.update( (n, (1, i)) for i, n in enumerate(X) ) # put nodes from X at x=1
        pos.update( (n, (2, i)) for i, n in enumerate(Y) ) # put nodes from Y at x=2
        nx.draw(B, pos=pos, with_labels=True)
        self.canvas.draw_idle()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':

    import sys  
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    app.setStyle(QStyleFactory.create("gtk"))
    screen = PrettyWidget() 
    screen.show()   
    sys.exit(app.exec_())# -*- coding: utf-8 -*-

"""Main module."""
