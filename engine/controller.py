from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot


class GameController(QObject):
    controller_signal_to_model = pyqtSignal(str)
    controller_signal_to_view = pyqtSignal(str)

    def __init__(self, view, model, thread):
        """Initialize the controller with the given view, model, and thread.

        Connect signals and slots to enable communication between the different
        components of the game:
        - MODEL signal is connected to CONTROLLER slot to get game responses,
        which are then sent to VIEW via `on_model_signal` method.
        - VIEW signal is connected to CONTROLLER slot to get user input, which
        is then sent to MODEL via `on_view_signal` method.
        - CONTROLLER signal is connected to MODEL slot to send user actions,
        which are then handled by `handle_inbound_signal` method.
        - CONTROLLER signal is connected to the VIEW slots to send game
        responses, which are then displayed by `handle_game_response` method.

        Parameters
        ----------
        view : GameView
            The view component of the game.
        model : GameModel
            The model component of the game.
        thread : GameThread
            The thread used to run the game loop.
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
