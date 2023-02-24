from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

import world
from player import Player

class Game(QObject):
    model_signal_to_controller = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.play()
        self.output = None
        self.action = None

    def play(self):
        """
        - Send outbound signal with instructions to controller
        - Wait for controller response
        - Get inbound signal with response from controller
        - Parse response to select instruction to send as signal
            
        """
        world.parse_world_dsl()
        player = Player()

        self.output = "***** INTRUDER *****"
        self.handle_outbound_signal(self.output)

        self.action = self.model_signal_to_controller
        if self.action in ["Talk"]:
            self.output = "HI!"
            self.handle_outbound_signal(self.output)
        else:
            self.output = "I beg you pardon?!"
            self.handle_outbound_signal(self.output)

    @pyqtSlot(str)
    def handle_inbound_signal(self, input):
        ''' Takes a string an send it to controller as a signal '''
        
        print(f"I'm MODEL and I got a signal from CONTROLLER: {input}")

    def handle_outbound_signal(self, output):
        ''' Takes a string an send it to controller as a signal '''
        
        print(f"I'm MODEL and I'm sending a signal to CONTROLLER: {output}")
        self.model_signal_to_controller.emit(output)
