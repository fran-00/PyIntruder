from PyQt6.QtGui import QAction, QIcon

from .game_gui import GameGUI


class GameMenu(GameGUI):
    def __init__(self, game_view):
        super().__init__(game_view)
        self.menubar = self.game_view.menuBar()

    def create_file_menu(self):
        file_menu = self.menubar.addMenu("File")
        self.add_menu_action(file_menu, self.new_game, "New Game")
        self.add_menu_action(file_menu, self.on_save, "Save")
        self.add_menu_action(file_menu, self.on_save_as, "Save As...")
        self.add_menu_action(file_menu, self.on_reload, "Reload")
        self.add_menu_action(file_menu, self.game_view.close, "Exit")

    def add_menu_action(self, menu, action, text):
        menu_action = QAction(text, self.game_view)
        menu_action.triggered.connect(action)
        menu.addAction(menu_action)

    def new_game(self):
        pass

    def on_save(self):
        pass

    def on_save_as(self):
        pass

    def on_reload(self):
        pass
