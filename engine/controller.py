from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot


class GameController(QObject):
    controller_signal_to_model = pyqtSignal(str)
    controller_signal_to_view = pyqtSignal(str)

    def __init__(self, view, model, thread):
        """Initialize the controller with the given view, model, and thread.

        Connects signals and slots to enable communication between the different components of the game:
        - The MODEL signals are connected to the CONTROLLER slots to get game responses, which are then sent to the VIEW via the `on_model_signal` method.
        - The VIEW signals are connected to the CONTROLLER slots to get user input, which is then sent to the MODEL via the `on_view_signal` method.
        - The CONTROLLER signals are connected to the MODEL slots to send user actions, which are then handled by the `handle_inbound_signal` method.
        - The CONTROLLER signals are also connected to the VIEW slots to send game responses, which are then displayed by the `handle_game_response` method.

        Args:
            view (GameView): The view component of the game.
            model (GameModel): The model component of the game.
            thread (GameThread): The thread used to run the game loop.

        Returns:
            None

        """
        super().__init__()

        model.model_signal_to_controller.connect(self.on_model_signal)
        view.view_signal_to_controller.connect(self.on_view_signal)
        self.controller_signal_to_model.connect(model.handle_inbound_signal)
        self.controller_signal_to_view.connect(view.handle_game_response)

        # Starts Game threads
        thread.start()

    @pyqtSlot(str)
    def on_model_signal(self, data):
        """Process data received from the MODEL and send it to VIEW"""
        self.controller_signal_to_view.emit(data)

    @pyqtSlot(str)
    def on_view_signal(self, data):
        """ Process data received from the VIEW and send it to MODEL"""
        self.controller_signal_to_model.emit(data)
