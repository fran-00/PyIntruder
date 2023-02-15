import sys, random
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt6.QtCore import pyqtSignal, pyqtSlot

class GameView(QWidget):
    controller_signal = pyqtSignal(str)
    
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
        self.input_box.returnPressed.connect(self.handle_input)
        self.input_box.returnPressed.connect(self.handle_output)

        # Button to submit input
        self.send_button = QPushButton("Enter")
        self.send_button.clicked.connect(self.handle_input)

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

    def handle_input(self):
        # Gets user input
        user_input = self.input_box.text().strip()
        
        # Emits the signal that contains user input
        self.controller_signal.emit(user_input)

        # Append user input to log view window
        self.log_view.append(f"Input: {user_input}")

        # Resets the input box
        self.input_box.clear()
        self.input_box.setFocus()
    
    def handle_output(self):
        # Responds to the user
        response = str(random.randint(1, 100000))
        
        # Append game output to log view window
        self.log_view.append(f"Output: {response}")
    
        # Emits the signal that contains game response
        self.controller_signal.emit(response)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    game_window = GameView()
    game_window.show()

    sys.exit(app.exec())
    
    