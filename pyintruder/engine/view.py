from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit
from PyQt6.QtCore import pyqtSignal, pyqtSlot

from ..gui.widgets import GameButtons, GameEntry
from ..gui.game_bars import GameMenu, GameProgressBars


class GameView(QMainWindow):
    view_signal_to_controller = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyIntruder")
        self.resize(1024, 768)
        self.setStyleSheet(self.load_css_file())
        self.create_layout()
        GameMenu(self).create_file_menu()

    def create_layout(self):
        """Create a vertical layout for the window"""
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        log_view = self.on_log_view()
        input_layout = GameEntry(self).on_input_layout()
        buttons_layout = GameButtons(self).on_parent_buttons_layout()
        self.health_bar = GameProgressBars(self).create_health_bar()
        self.mana_bar = GameProgressBars(self).create_mana_bar()

        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(self.health_bar)
        main_layout.addWidget(self.mana_bar)
        main_layout.addWidget(log_view)
        main_layout.addLayout(input_layout)
        main_layout.addLayout(buttons_layout)
        # Set focus on input box
        self.input_box.setFocus()

    def on_log_view(self):
        """Add widget for displaying inputs and outputs"""
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.ensureCursorVisible()

        return self.log_view

    def get_game_log(self):
        return self.log_view.toPlainText()

    def handle_user_action(self, command):
        action = self.input_box.text().strip() if command == "none" else command
        return self.close() if action.lower() == "quit" else self.process_action(action)

    def process_action(self, action):
        # Emits the signal that contains user input
        self.view_signal_to_controller.emit(action)
        # Append user input to log view window
        self.log_view.append(
            f"<p style='color:#ffdc7d; font-weight:600'>>>> {action}</p>")
        # Resets the input box
        self.input_box.clear()
        self.input_box.setFocus()

    def load_css_file(self):
        with open("pyintruder/gui/styles/styles.css", "r") as file:
            return file.read()

    @pyqtSlot(str)
    def handle_game_response(self, response):
        """ Slot that receives a string from controller as a signal """
        # Append game output to log view window
        self.log_view.append(f"{response}")

    @pyqtSlot(tuple)
    def update_game_bars(self, player_data):
        """
        Slot that receives a tuple from controller to update status bars
        with player infos.
        """
        player_hp = player_data[0]
        player_max_hp = player_data[1]
        player_mana = player_data[2]
        player_max_mana = player_data[3]
        self.health_bar.setMaximum(player_max_hp)
        self.health_bar.setValue(player_hp)
        self.mana_bar.setMaximum(player_max_mana)
        self.mana_bar.setValue(player_mana)
