import sys

from PyQt6.QtWidgets import QApplication

import old_world_gen as world
from engine.model import GameModel
from engine.view import GameView
from engine.controller import GameController
from entities.player import Player
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    world.parse_world_dsl()
    player = Player()
    view = GameView()
    model = GameModel(player)
    controller = GameController(view, model)
    view.show()

    sys.exit(app.exec())

