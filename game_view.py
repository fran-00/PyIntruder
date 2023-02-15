import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton
from PyQt6.QtCore import pyqtSignal, pyqtSlot

class GameView(QWidget):
    controller_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Window")
        self.resize(600, 400)

        # Widget per la visualizzazione di input e output
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.ensureCursorVisible()

        # Widget per l'input
        self.input_box = QLineEdit()
        self.input_box.returnPressed.connect(self.handle_input)

        # Bottone per inviare l'input
        self.send_button = QPushButton("Enter")
        self.send_button.clicked.connect(self.handle_input)

        # Layout orizzontale per input box e bottone
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_button)

        # Layout verticale per la finestra
        layout = QVBoxLayout()
        layout.addWidget(self.log_view)
        layout.addLayout(input_layout)
        self.setLayout(layout)
        
        # Foglio di stile
        self.setStyleSheet("color: white; background-color: black;")

    def handle_input(self):
        # Ottiene l'input dell'utente
        user_input = self.input_box.text().strip()
        
        # Emette il segnale che contiene l'input dell'utente
        self.controller_signal.emit(user_input)

        # Mostra l'input dell'utente
        self.log_view.append(f"Input: {user_input}")

        # Risponde all'utente
        response = "I beg your pardon?"
        self.log_view.append(f"Output: {response}")

        # Resetta l'input box
        self.input_box.clear()
        self.input_box.setFocus()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    game_window = GameView()
    game_window.show()

    sys.exit(app.exec())
    
    