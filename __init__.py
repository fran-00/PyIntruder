import sys

from PyQt6.QtWidgets import QApplication

from engine.model import GameModel
from engine.game_view import GameView
from engine.controller import GameController
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    game_view = GameView()
    game_model = GameModel()
    game_controller = GameController(game_view, game_model)
    game_view.show()

    sys.exit(app.exec())

