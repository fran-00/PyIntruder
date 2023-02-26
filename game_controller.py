from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

class GameController(QObject):
    controller_signal_to_model = pyqtSignal(str)
    controller_signal_to_view = pyqtSignal(str)

    def __init__(self, game_view, game_model):
        '''
        CONNECTS SLOTS AND SIGNALS:
        - CONTROLLER gets game response from MODEL
        - CONTROLLER sends game response to VIEW
        - CONTROLLER gets user action from VIEW
        - CONTROLLER send user action to MODEL
        '''
        super().__init__()
        
        # Connect MODEL signals to CONTROLLER slots to get game
        # response and send it to VIEW via on_model_signal method
        game_model.model_signal_to_controller.connect(self.on_model_signal)
        
        # Connect VIEW signals to CONTROLLER slots to get user
        # input and send it to MODEL via on_view_signal method
        game_view.view_signal_to_controller.connect(self.on_view_signal)
        
        # Connect CONTROLLER signals to MODEL slots to send user action,
        # then handle_inbound_signal method will send them to gameloop
        self.controller_signal_to_model.connect(game_model.handle_inbound_signal)
        
        # FIXME: this doesn't work
        # Connect CONTROLLER signals to VIEW slots to send game response
        # then ??? will show them and wait for new user input 
        self.controller_signal_to_view.connect(game_view.handle_game_response)


    @pyqtSlot(str)
    def on_model_signal(self, data):
        # Process data received from the MODEL and send it to VIEW
        print(f"I'm is CONTROLLER and I'm receiving a signal from MODEL that says {data}!")
        self.controller_signal_to_view.emit(data)

    @pyqtSlot(str)
    def on_view_signal(self, data):
        # Process data received from the VIEW and send it to MODEL
        print(f"I'm CONTROLLER and I got a signal from VIEW that says: {data}")
        self.controller_signal_to_model.emit(data)



