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
        loop = QEventLoop()
        world.parse_world_dsl()
        player = Player()
 
        while player.is_alive:
            # Il model riceve l'azione dell'utente dalla view
            user_action = None
            while not user_action:
                loop.processEvents()
                if self.action:
                    user_action = self.action
                    self.action = None

            # Il model processa l'azione dell'utente e genera una risposta
            game_response = "I beg you pardon?"

            # Il model invia la risposta alla view
            self.model_signal_to_controller.emit(game_response)

            # Il model controlla se il giocatore è vivo e passa al prossimo turno
            if not player.is_alive:
                break

    @pyqtSlot(str)
    def handle_inbound_signal(self, user_action):
        ''' Slot that receives a string from controller as a signal '''
        self.action = user_action
        
        print(f"MODEL: I got a signal from CONTROLLER with user action: {user_action}")
        return user_action

    def handle_outbound_signal(self, game_response):
        ''' Takes a string an send it to controller as a signal '''
        # Test game response
        # game_response = "HI"
        
        print(f"MODEL: I'm sending a signal to CONTROLLER with game response: {game_response}")
        # Emits the signal that contains game response
        self.model_signal_to_controller.emit(game_response)
        
        