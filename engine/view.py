from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit
from PyQt6.QtCore import pyqtSignal, pyqtSlot

from gui.widgets import GameButtons, GameEntry
from gui.menubar import GameMenu
from gui.status_bars import HealthBar


class GameView(QMainWindow):
    view_signal_to_controller = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyIntruder")
        self.resize(1024, 768)
        self.create_layout()
        GameMenu(self).create_file_menu()

    def create_layout(self):
        """Create a vertical layout for the window"""
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.on_log_view())
        layout.addLayout(GameEntry(self).on_input_layout())
        layout.addLayout(GameButtons(self).on_movements_buttons())
        layout.addLayout(GameButtons(self).on_actions_buttons())

        # TODO: Add player health bar
        # prograss_bar = HealthBar(self).crete_health_bar()
        # layout.addWidget(prograss_bar)

    def on_log_view(self):
        """Add widget for displaying inputs and outputs"""
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.ensureCursorVisible()

        return self.log_view

    def handle_user_action(self, command):
        if command == "none":
            action = self.input_box.text().strip()
        else:
            action = command

        # Emits the signal that contains user input
        self.view_signal_to_controller.emit(action)

        # Append user input to log view window
        self.log_view.append(f"<p style='color:#ffdc7d; font-weight:600'>>>> {action}</p>")

        # Resets the input box
        self.input_box.clear()
        self.input_box.setFocus()

    @pyqtSlot(str)
    def handle_game_response(self, response):
        """ Slot that receives a string from controller as a signal """
        # Append game output to log view window
        self.log_view.append(f"{response}")
