import os.path
import pkg_resources
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ScotlandPYard.resources.gameconfig import stylesheet


class ScotlandPYardGame(QWidget):
    NumButtons = ['btn' + str(i) for i in range(1, 32)]

    def __init__(self):

        super(ScotlandPYardGame, self).__init__()
        self.resourcepath = pkg_resources.resource_filename("ScotlandPYard.resources", "images")
        iconpath = os.path.join(self.resourcepath, "icon.png")
        self.setWindowIcon(QIcon(iconpath))
        self.canvas = QLabel()

        font = QFont()
        font.setPointSize(16)
        self.initUI()

    def initUI(self):

        self.setGeometry(100, 100, 800, 800)
        self.center()
        self.setWindowTitle('S. pyard')

        mainlayout = QHBoxLayout()
        self.setLayout(mainlayout)

        self.createThiefMovesGroupBox()
        self.createPlayersDashHBox()

        self.createLeftBox()

        mainlayout.addWidget(self.leftBox, 1)
        mainlayout.addWidget(self.thiefMovesGroupBox)

        self.showMap()

        self.show()

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
        for i in range(1, 5):
            playerDash = self.getNewPlayerDash("Detective " + str(i))
            layout.addWidget(playerDash)

        # add Mr. X
        playerDash = self.getNewPlayerDash("Mr. X")
        layout.addWidget(playerDash)
        self.playersDashHBox.setLayout(layout)

    def getNewPlayerDash(self, playerName):
        items = {'Taxi': 10, 'Bus': 8, 'Underground': 5}
        playerDash = QGroupBox(playerName)

        layout = QVBoxLayout()
        for k, v in items.items():
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
        pixmap = QPixmap(os.path.join(self.resourcepath, 'map.jpg'))
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
