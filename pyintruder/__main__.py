import sys

from PyQt6.QtWidgets import QApplication

from pyintruder.world.parser import WorldCreator
from pyintruder.engine.model import GameModel, GameThread
from pyintruder.engine.view import GameView
from pyintruder.engine.controller import GameController
from pyintruder.entities.player import Player


def main():
    app = QApplication(sys.argv)
    WorldCreator.parse_world_dsl()
    player = Player()
    view = GameView()
    model = GameModel(player)
    thread = GameThread(model)
    controller = GameController(view, model, thread)
    view.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
