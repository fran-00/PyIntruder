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
        layout.addLayout(self.on_movements_buttons())
        self.setLayout(layout)

        # Modify Style Sheet
        self.setStyleSheet("color: white; background-color: black;")

    def on_movements_buttons(self):
        """Add buttons for cardinal directions to game GUI"""
        self.button_north = QPushButton("North")
        self.button_south = QPushButton("South")
        self.button_east = QPushButton("East")
        self.button_west = QPushButton("West")
        
        # Connect direction buttons to a common handler
        self.button_north.clicked.connect(lambda: self.view_signal_to_controller.emit("n"))
        self.button_south.clicked.connect(lambda: self.view_signal_to_controller.emit("s"))
        self.button_east.clicked.connect(lambda: self.view_signal_to_controller.emit("e"))
        self.button_west.clicked.connect(lambda: self.view_signal_to_controller.emit("w"))

        # Horizontal layout for direction buttons
        direction_layout = QHBoxLayout()
        direction_layout.addWidget(self.button_north)
        direction_layout.addWidget(self.button_south)
        direction_layout.addWidget(self.button_east)
        direction_layout.addWidget(self.button_west)
        
        return(direction_layout)

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
