from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
import random

class GameController(QObject):
    controller_signal_to_model = pyqtSignal(str)
    controller_signal_to_view = pyqtSignal(str)

    def __init__(self, game_view, game_model):
        super().__init__()
        
        # Connect model signals to controller slots
        game_model.model_signal_to_controller.connect(self.on_model_signal)

        # Connect view signals to controller slots
        game_view.view_signal_to_controller.connect(self.on_view_signal)

    @pyqtSlot(str)
    def on_model_signal(self, data):
        # Process data received from the model
        print("My name is CONTROLLER and I'm receiving a signal from MODEL!")
        # Send data to the view
        self.controller_signal_to_view.emit(data)

    @pyqtSlot(str)
    def on_view_signal(self, data):
        # Process data received from the view
        print("I'm CONTROLLER and I got a signal from VIEW!")
        print(f"The signal says: {data}")
        print("Now I add some numbers and send the signal to MODEL...")
        x = str(random.randint(0, 1000))
        data_changed = data + x

        # Send data to the model
        # self.controller_signal_to_model.emit(data)
        
        self.controller_signal_to_model.emit(data_changed)
