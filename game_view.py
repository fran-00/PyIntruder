from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton

class GameView(QWidget):
    input_submitted = pyqtSignal(str)

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

        # Bottone per inviare l'input
        self.send_button = QPushButton("Enter")

        # Layout orizzontale per input box e bottone
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_button)

        # Layout verticale per la finestra
        layout = QVBoxLayout()
        layout.addWidget(self.log_view)
        layout.addLayout(input_layout)
        self.setLayout(layout)
        
        # Foglio di stile con i colori
        self.setStyleSheet("color: white; background-color: black;")

        # Connessioni ai segnali
        self.input_box.returnPressed.connect(self.handle_input)
        self.send_button.clicked.connect(self.handle_input)

    def handle_input(self):
        # Ottiene l'input dell'utente
        user_input = self.input_box.text().strip()

        if user_input.lower() == "quit":
            # Chiude la finestra se l'utente ha inserito "quit"
            self.close()
            return

        # Invia il segnale con l'input dell'utente
        self.input_submitted.emit(user_input)

        # Resetta l'input box
        self.input_box.clear()
        self.input_box.setFocus()

    def display_output(self, output):
        # Mostra l'output nel log view
        self.log_view.append(f"Output: {output}")

