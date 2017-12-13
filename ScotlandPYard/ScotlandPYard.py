import os.path
import pkg_resources
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ScotlandPYard.resources.gameconfig import stylesheet
from ScotlandPYard.spyengine.engine import Game


class ScotlandPYardGame(QWidget):
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

        self.engine = None
        self.game_state = None

        font = QFont()
        font.setPointSize(16)
        self.createDummyGame()
        self.initUI()

    def initUI(self):

        self.setGeometry(100, 100, 800, 800)
        self.center()
        self.setWindowTitle('S. pyard')

        mainlayout = QHBoxLayout()
        self.setLayout(mainlayout)

        self.refresh_game_state()
        self.createThiefMovesGroupBox()
        self.createPlayersDashHBox()

        self.createLeftBox()

        mainlayout.addWidget(self.leftBox, 1)
        mainlayout.addWidget(self.thiefMovesGroupBox)

        self.show()
        self.showMap()

    def refresh_game_state(self):
        if self.engine is not None:
            self.game_state = self.engine.get_game_state()

    def createDummyGame(self):
        self.engine = Game()

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
        # add detectives
        for d in self.game_state["detectives"]:
            playerDash = self.getNewPlayerDash(d)
            layout.addWidget(playerDash)

        # add Mr. X
        playerDash = self.getNewPlayerDash(self.game_state["Mr. X"])
        layout.addWidget(playerDash)

        self.playersDashHBox.setLayout(layout)

    def getNewPlayerDash(self, player):
        # items = {'Taxi': 10, 'Bus': 8, 'Underground': 5}
        displayname = player["name"]
        if player["is_ai"]:
            displayname += " (AI)"
        playerDash = QGroupBox(displayname)

        layout = QVBoxLayout()
        for k, v in player["tickets"].items():
            button = QPushButton("{} x{}".format(k, v))
            button.setObjectName(k)
            button.setStyleSheet(stylesheet[k])
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
        # Create widget
        pixmap = QPixmap(os.path.join(self.resourcepath, 'map3.jpg'))
        pixmap = pixmap.scaled(self.canvas.size())
        self.canvas.setPixmap(pixmap)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def resizeEvent(self, event):
        self.showMap()


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
