import sys

from PyQt6.QtWidgets import QApplication

from world.parser import WorldCreator
from engine.model import GameModel, GameThread
from engine.view import GameView
from engine.controller import GameController
from entities.player import Player


if __name__ == '__main__':
    app = QApplication(sys.argv)
    WorldCreator.parse_world_dsl()
    player = Player()
    view = GameView()
    model = GameModel(player)
    thread = GameThread(model)
    controller = GameController(view, model, thread)
    view.show()

    sys.exit(app.exec())
