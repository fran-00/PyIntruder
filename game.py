from PyQt6.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, QEventLoop

import world
from player import Player
from game_logic import GameLogic


class GameThread(QThread):
    def __init__(self, game_model):
        super().__init__()
        self.game_model = game_model

    def run(self):
        self.game_model.play()
        

class Game(QObject):
    model_signal_to_controller = pyqtSignal(str)
    
    def __init__(self):
        self.action = None
        self.response = None
        self.event_loop = None
        super().__init__()

    def play(self):
        """
        - Send outbound signal with instructions to controller
        - Wait for controller response
        - Get inbound signal with response from controller
        - Parse response to select instruction to send as signal
        """
        self.event_loop = QEventLoop()
        world.parse_world_dsl()
        player = Player()
        logic = GameLogic()
 
        while True:
            game_response = self.get_game_response(logic)
            print(f"MODEL: Game response is: {game_response}")
            self.model_signal_to_controller.emit(game_response)
            self.event_loop.exec()

    @pyqtSlot(str)
    def handle_inbound_signal(self, user_action):
        ''' Slot that receives a string from controller as a signal '''
        self.action = user_action
        
        print(f"MODEL: I got a signal from CONTROLLER with user action: {user_action}")
        
        self.event_loop.exit()


    def handle_outbound_signal(self, game_response):
        ''' Takes a string an send it to controller as a signal '''
        
        print(f"MODEL: I'm sending a signal to CONTROLLER with game response: {game_response}")
        
        # Emits the signal that contains game response
        self.model_signal_to_controller.emit(game_response)


    def get_game_response(self, logic):
        game_response = logic.choose_action(self.action)
        return game_response
    
    
    def get_room_descriprion(self, logic):
        return(logic.check_tile())