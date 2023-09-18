from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QProgressBar


class GameProgressBars:
    def __init__(self, game_view):
        self.game_view = game_view

    def crete_health_bar(self):
        self.health_bar = QProgressBar(self.game_view, objectName="health_bar")
        return self.health_bar

    def crete_mana_bar(self):
        self.mana_bar = QProgressBar(self.game_view, objectName="mana_bar")
        return self.mana_bar


class GameMenu:
    def __init__(self, game_view):
        self.game_view = game_view
        self.menubar = self.game_view.menuBar()

    def create_file_menu(self):
        file_menu = self.menubar.addMenu("File")
        self.add_menu_action(file_menu, self.new_game, "New Game")
        self.add_menu_action(file_menu, lambda: self.game_view.handle_user_action("save"), "Save")
        self.add_menu_action(file_menu, self.on_save_as, "Save As...")
        self.add_menu_action(file_menu, lambda: self.game_view.handle_user_action("reload"), "Reload")
        self.add_menu_action(file_menu, self.on_export_game, "Export Game")
        self.add_menu_action(file_menu, self.game_view.close, "Exit")

    def add_menu_action(self, menu, action, text):
        menu_action = QAction(text, self.game_view)
        menu_action.triggered.connect(action)
        menu.addAction(menu_action)

    def new_game(self):
        pass

    def on_save_as(self):
        pass

    def on_export_game(self):
        pass
