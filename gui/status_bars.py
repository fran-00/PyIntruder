from PyQt6.QtWidgets import QProgressBar

from .game_gui import GameGUI
from entities.player import Player


class HealthBar(GameGUI):
    def __init__(self, game_view):
        super().__init__(game_view)

    def crete_health_bar(self):
        self.health_bar = QProgressBar(self.game_view)
        return self.health_bar
