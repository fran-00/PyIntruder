from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, QEventLoop

import world
from player import Player

class Game(QObject):
    model_signal_to_controller = pyqtSignal(str)
    
    def __init__(self):
        self.action = None
        self.response = None
        super().__init__()
        self.play()

    def play(self):
        """
        - Send outbound signal with instructions to controller
        - Wait for controller response
        - Get inbound signal with response from controller
        - Parse response to select instruction to send as signal
        """
        world.parse_world_dsl()
        player = Player()
        
        self.response = "***** INTRUDER *****"
 

    @pyqtSlot(str)
    def handle_inbound_signal(self, user_action):
        ''' Slot that receives a string from controller as a signal '''
        
        print(f"MODEL: I got a signal from CONTROLLER with user action: {user_action}")
        self.action = user_action

    def handle_outbound_signal(self):
        ''' Takes a string an send it to controller as a signal '''
        # Test game response
        game_response = "HI"
        
        print(f"MODEL: I'm sending a signal to CONTROLLER with game response: {game_response}")
        # Emits the signal that contains game response
        self.model_signal_to_controller.emit(game_response)
        
        