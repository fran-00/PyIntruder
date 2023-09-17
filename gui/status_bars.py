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
