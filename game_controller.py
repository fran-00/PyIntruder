from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

class GameController(QObject):
    model_signal = pyqtSignal(str)
    view_signal = pyqtSignal(str)

    def __init__(self, game_view):
        super().__init__()
        
        # Connect model signals to controller slots
        # game.model_signal.connect(self.on_model_signal)

        # Connect view signals to controller slots
        game_view.controller_signal.connect(self.on_view_signal)

    @pyqtSlot(str)
    def on_model_signal(self, data):
        # Process data received from the model
        print("My name is CONTROLLER and I'm receiving a signal from MODEL!")
        # Send data to the view
        self.view_signal.emit(data)

    @pyqtSlot(str)
    def on_view_signal(self, data):
        # Process data received from the view
        print("My name is CONTROLLER and I'm receiving a signal from VIEW!")
        print(data)

        # Send data to the model
        self.model_signal.emit(data)