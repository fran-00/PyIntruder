from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt6.QtCore import pyqtSignal, pyqtSlot

from gui.widgets import GameButtons


class GameView(QWidget):
    view_signal_to_controller = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Window")
        self.resize(600, 400)

        # Vertical layout for the window
        layout = QVBoxLayout()
        layout.addWidget(self.on_log_view())
        layout.addLayout(self.on_input_layout())
        layout.addLayout(GameButtons(self).on_movements_buttons())
        layout.addLayout(GameButtons(self).on_actions_buttons())
        self.setLayout(layout)

    def on_log_view(self):
        """Add widget for displaying inputs and outputs"""
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.ensureCursorVisible()

        return self.log_view

    def on_input_layout(self):
        """Add horizzontal input box and a send button to submit"""
        self.input_box = QLineEdit()
        self.input_box.returnPressed.connect(lambda: self.handle_user_action("none"))

        # Button to submit input
        send_button = QPushButton("Enter")
        send_button.setProperty("class", "enter_button")
        send_button.clicked.connect(lambda: self.handle_user_action("none"))

        # Horizontal layout for input box and button
        input_layout = QHBoxLayout()
        input_layout.setProperty("class", "input_layout")
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(send_button)

        return input_layout

    def handle_user_action(self, command):
        if command == "none":
            action = self.input_box.text().strip()
        else:
            action = command

        # Emits the signal that contains user input
        self.view_signal_to_controller.emit(action)

        # Append user input to log view window
        self.log_view.append(f">>> {action}")

        # Resets the input box
        self.input_box.clear()
        self.input_box.setFocus()

    @pyqtSlot(str)
    def handle_game_response(self, response):
        """ Slot that receives a string from controller as a signal """
        # Append game output to log view window
        self.log_view.append(f"{response}")
