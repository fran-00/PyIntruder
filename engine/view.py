from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt6.QtCore import pyqtSignal, pyqtSlot


class GameView(QWidget):
    view_signal_to_controller = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Window")
        self.resize(600, 400)

        # Widget for displaying inputs and outputs
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.ensureCursorVisible()

        # Input widgets
        self.input_box = QLineEdit()
        self.input_box.returnPressed.connect(self.handle_user_action)

        # Button to submit input
        self.send_button = QPushButton("Enter")
        self.send_button.clicked.connect(self.handle_user_action)

        # Horizontal layout for input box and button
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_button)

        # Vertical layout for the window
        layout = QVBoxLayout()
        layout.addWidget(self.log_view)
        layout.addLayout(input_layout)
        self.setLayout(layout)

        # Modify Style Sheet
        self.setStyleSheet("color: white; background-color: black;")

    def handle_user_action(self):
        # Gets user input
        action = self.input_box.text().strip()

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
