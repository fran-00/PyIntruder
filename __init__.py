import sys

from PyQt6.QtWidgets import QApplication

from game_model import GameModel
from game_view import GameView
from game_controller import GameController
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    game_view = GameView()
    game_model = GameModel()
    game_controller = GameController(game_view, game_model)
    game_view.show()

    sys.exit(app.exec())

