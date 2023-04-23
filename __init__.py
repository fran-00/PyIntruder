import sys

from PyQt6.QtWidgets import QApplication

import world
from engine.model import GameModel
from engine.view import GameView
from engine.controller import GameController
from entities.player import Player
    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    view = GameView()
    model = GameModel()
    controller = GameController(view, model)
    view.show()

    sys.exit(app.exec())

