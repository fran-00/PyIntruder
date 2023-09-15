from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt6.QtCore import pyqtSignal, pyqtSlot


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
        layout.addLayout(self.on_movements_buttons())
        layout.addLayout(self.on_actions_buttons())
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

    def on_movements_buttons(self):
        """Add buttons for cardinal directions to game GUI"""
        button_north = QPushButton("🡅")
        button_south = QPushButton("🡇")
        button_east = QPushButton("🡆")
        button_west = QPushButton("🡄")

        buttons = [button_north, button_south, button_east, button_west]
        for button in buttons:
            button.setProperty("class", "cardinal_directions")

        # Connect direction buttons to a common handler
        button_north.clicked.connect(lambda: self.emit_command_from_button("n"))
        button_south.clicked.connect(lambda: self.emit_command_from_button("s"))
        button_east.clicked.connect(lambda: self.emit_command_from_button("e"))
        button_west.clicked.connect(lambda: self.emit_command_from_button("w"))

        # Horizontal layout for direction buttons
        direction_layout = QHBoxLayout()
        direction_layout.addWidget(button_north)
        direction_layout.addWidget(button_south)
        direction_layout.addWidget(button_east)
        direction_layout.addWidget(button_west)
        
        return direction_layout
    
    def on_actions_buttons(self):
        """Add buttons for actions to game GUI"""
        button_attack = QPushButton("Attack")
        button_curse = QPushButton("Cast Curse")
        button_inventory = QPushButton("Inventory")
        button_diagnose = QPushButton("Diagnose")

        button_attack.clicked.connect(lambda: self.emit_command_from_button("a"))
        button_curse.clicked.connect(lambda: self.emit_command_from_button("c"))
        button_inventory.clicked.connect(lambda: self.emit_command_from_button("i"))
        button_diagnose.clicked.connect(lambda: self.emit_command_from_button("diagnose"))

        command_layout = QHBoxLayout()
        command_layout.addWidget(button_attack)
        command_layout.addWidget(button_curse)
        command_layout.addWidget(button_inventory)
        command_layout.addWidget(button_diagnose)
        
        return command_layout

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
    
    def emit_command_from_button(self, command):
        self.view_signal_to_controller.emit(command)
        self.log_view.append(f">>> {command}")

    @pyqtSlot(str)
    def handle_game_response(self, response):
        """ Slot that receives a string from controller as a signal """
        # Append game output to log view window
        self.log_view.append(f"{response}")
