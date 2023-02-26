from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

class GameController(QObject):
    controller_signal_to_model = pyqtSignal(str)
    controller_signal_to_view = pyqtSignal(str)

    def __init__(self, game_view, game_model):
        super().__init__()
        
        # Connect model signals to controller slots
        game_model.model_signal_to_controller.connect(self.on_model_signal)
        # Connect controller signals to model slots
        self.controller_signal_to_model.connect(game_model.handle_inbound_signal)
        # Connect view signals to controller slots
        game_view.view_signal_to_controller.connect(self.on_view_signal)
        # Connect controller signals to view slots
        self.controller_signal_to_view.connect(game_view.handle_output)


    @pyqtSlot(str)
    def on_model_signal(self, data):
        # Process data received from the model
        print(f"I'm is CONTROLLER and I'm receiving a signal from MODEL that says {data}!")
        # Send data to the view
        self.controller_signal_to_view.emit(data)

    @pyqtSlot(str)
    def on_view_signal(self, data):
        # Process data received from the view
        print(f"I'm CONTROLLER and I got a signal from VIEW that says: {data}")

        # Send data to the model
        self.controller_signal_to_model.emit(data)


