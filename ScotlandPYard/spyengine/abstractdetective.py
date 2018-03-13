import pkg_resources
from PyQt5.QtSvg import QGraphicsSvgItem
from numpy.random import choice
from os.path import join

from ScotlandPYard.config.gameconfig import icons
from .abstractplayer import AbstractPlayer


class AbstractDetective(AbstractPlayer):
    def __init__(self, engine, is_ai=False, name=None):
        super().__init__(engine, is_ai=is_ai)

        icon = choice(icons)
        if name is None:
            name = "Detective " + icon.capitalize()

        iconspath = pkg_resources.resource_filename("ScotlandPYard.resources", "icons")
        iconpath = join(iconspath, icon + ".svg")

        self.icon = QGraphicsSvgItem(iconpath)
        self.icon.setScale(0.05)
        self.name = name
        self.tickets = {
            "Bus": 8,
            "Taxi": 10,
            "Underground": 4
        }

    def get_role(self):
        return "detective"
