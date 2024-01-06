from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QProgressBar


class GameProgressBars:
    def __init__(self, game_view):
        self.game_view = game_view

    def create_health_bar(self):
        self.health_bar = QProgressBar(self.game_view, objectName="health_bar")
        return self.health_bar

    def create_mana_bar(self):
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
        self.add_menu_action(file_menu, self.on_export_game_log, "Export Game")
        self.add_menu_action(file_menu, self.game_view.close, "Exit")

    def add_menu_action(self, menu, action, text):
        menu_action = QAction(text, self.game_view)
        menu_action.triggered.connect(action)
        menu.addAction(menu_action)

    def new_game(self):
        pass

    def on_save_as(self):
        pass

    def on_export_game_log(self):
        self.game_view.handle_user_action("export")
        game_log = self.game_view.get_game_log()
        file_path = "game_log.txt"
        with open(file_path, 'w') as file:
            file.write(game_log)
