from PyQt6.QtWidgets import QProgressBar

from .game_gui import GameGUI
from entities.player import Player


class HealthBar(GameGUI):
    def __init__(self, game_view):
        super().__init__(game_view)
        self.player = Player()

    def crete_health_bar(self):
        health_bar = QProgressBar(self.game_view)
        health_bar.setValue(self.player.max_hp)

        return health_bar

    def process_player_data(self, player_hp, player_max_hp):
        pass
