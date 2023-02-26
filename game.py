from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QEventLoop


class Game(QObject):
    model_signal_to_controller = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.play()

    def play(self):
        """
        - Send outbound signal with instructions to controller
        - Wait for controller response
        - Get inbound signal with response from controller
        - Parse response to select instruction to send as signal
        """
        self.output = "***** INTRUDER *****"
        self.handle_outbound_signal(self.output)


    @pyqtSlot(str)
    def handle_inbound_signal(self, user_action):
        ''' Slot that receives a string from controller as a signal '''
        
        print(f"I'm MODEL and I got a signal from CONTROLLER: {user_action}")
        self.action = user_action

    def handle_outbound_signal(self, game_response):
        ''' Takes a string an send it to controller as a signal '''
        
        print(f"I'm MODEL and I'm sending a signal to CONTROLLER: {game_response}")
        self.model_signal_to_controller.emit(game_response)
