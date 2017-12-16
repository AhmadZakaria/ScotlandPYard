import os.path

# from PyQt5.QtOpenGL import *
import pkg_resources
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ScotlandPYard.resources.stylesheet import stylesheet
from ScotlandPYard.spyengine.engine import Game
from ScotlandPYard.spymap import SPYMap


class ScotlandPYardGame(QMainWindow):
    NumButtons = [str(i) for i in range(1, 31)]
    revealedstates = [2, 8, 14, 20, 29]
    for i in revealedstates:
        NumButtons[i] = "({})".format(NumButtons[i])

    def __init__(self):

        super(ScotlandPYardGame, self).__init__()
        self.resourcepath = pkg_resources.resource_filename("ScotlandPYard.resources", "images")
        iconpath = os.path.join(self.resourcepath, "icon.png")
        self.setWindowIcon(QIcon(iconpath))
        self.canvas = QLabel()
        self.grview = QGraphicsView()
        # self.grview.setViewport(QGLWidget())

        self.spymap = SPYMap(map_name='map3')

        self.engine = None
        self.game_state = None

        font = QFont()
        font.setPointSize(16)
        self.initGameEngine()
        self.initUI()

    def initUI(self):

        self.setGeometry(100, 100, 800, 800)
        self.center()
        self.setWindowTitle('S. pyard')

        self.statusBar()

        centralWidget = QWidget()
        mainlayout = QHBoxLayout()

        # Set the Layout
        centralWidget.setLayout(mainlayout)

        # Set the Widget
        self.setCentralWidget(centralWidget)

        self.createThiefMovesGroupBox()
        self.createPlayersDashHBox()
        self.refresh_game_state()

        self.createLeftBox()

        mainlayout.addWidget(self.leftBox, 1)
        mainlayout.addWidget(self.thiefMovesGroupBox)

        self.show()
        self.showMap()

    def refresh_game_state(self):
        if self.engine is not None:
            self.game_state = self.engine.get_game_state()
            turn = self.game_state["turn"]
            loc = self.game_state["players_state"][turn]["location"]
            self.spymap.set_player_turn(loc)

            for i, layout in enumerate(self.playersDashHBox.findChildren(QGroupBox)):
                layout.setEnabled(turn == i)

    def initGameEngine(self):
        self.engine = Game(graph=self.spymap.graph)
        self.game_state = self.engine.get_game_state()

    def createThiefMovesGroupBox(self):
        self.thiefMovesGroupBox = QGroupBox()

        layout = QVBoxLayout()
        for i in self.NumButtons:
            button = QPushButton(i)
            button.setObjectName(i)
            layout.addWidget(button)
            self.thiefMovesGroupBox.setLayout(layout)

    #       button.clicked.connect(self.submitCommand)

    def createPlayersDashHBox(self):
        self.playersDashHBox = QGroupBox()

        layout = QHBoxLayout()
        # add players
        for d in self.game_state["players_state"]:
            playerDash = self.getNewPlayerDash(d)

            layout.addWidget(playerDash)

        self.playersDashHBox.setLayout(layout)

    def getNewPlayerDash(self, player):
        displayname = player["name"]
        if player["is_ai"]:
            displayname += " (AI)"
        playerDash = QGroupBox(displayname)

        layout = QVBoxLayout()
        for k, v in player["tickets"].items():
            button = QPushButton("{} ({})".format(k, v))
            button.setObjectName(k)
            button.setStyleSheet(stylesheet[k])
            button.clicked.connect(self.submitCommand)
            button.setProperty("player", player)
            layout.addWidget(button)
            playerDash.setLayout(layout)
        return playerDash

    def createLeftBox(self):
        self.leftBox = QGroupBox()
        layout = QVBoxLayout()
        layout.addWidget(self.spymap, 1)
        layout.addWidget(self.playersDashHBox)
        self.leftBox.setLayout(layout)

    def showMap(self):
        self.spymap.update()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def resizeEvent(self, event):
        self.showMap()

    def submitCommand(self):
        sender = self.sender()
        player = sender.property("player")
        self.statusBar().showMessage(sender.objectName() + ": " + player["name"] + ' was pressed')
        valid_nodes = self.engine.get_valid_nodes(player_name=player["name"], ticket=sender.objectName())
        self.spymap.highlight_nodes(valid_nodes)


def main():
    import sys
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    app.setStyle(QStyleFactory.create("gtk"))
    screen = ScotlandPYardGame()
    screen.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
