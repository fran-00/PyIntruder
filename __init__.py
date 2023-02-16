import sys

from PyQt6.QtWidgets import QApplication

from game import Game
from game_view import GameView
from game_controller import GameController
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # game_model = Game()
    game_view = GameView()
    game_controller = GameController(game_view)
    game_view.show()

    sys.exit(app.exec())

