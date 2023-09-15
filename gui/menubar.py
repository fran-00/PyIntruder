from PyQt6.QtGui import QAction, QIcon

class GameMenu:
    def __init__(self, game_view):
        self.game_view = game_view

    def create_menu(self):
        menubar = self.game_view.menuBar()
        file_menu = menubar.addMenu("File")

        exit_action = QAction("Exit", self.game_view)
        exit_action.triggered.connect(self.game_view.close)
        file_menu.addAction(exit_action)
