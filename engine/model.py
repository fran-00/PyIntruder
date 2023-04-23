from collections import OrderedDict

from PyQt6.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, QEventLoop

import world


class GameThread(QThread):
    def __init__(self, game_model):
        super().__init__()
        self.game_model = game_model

    def run(self):
        self.game_model.play()
        

class GameModel(QObject):
    model_signal_to_controller = pyqtSignal(str)
    
    def __init__(self, player):
        self.player = player
        self.action = None
        self.room = None
        super().__init__()

    def play(self):
        """
        - Send outbound signal with instructions to controller
        - Wait for controller response
        - Get inbound signal with response from controller
        - Parse response to select instruction to send as signal
        """
        self.event_loop = QEventLoop()
 
        while True:
            game_response = self.get_game_response()
            self.model_signal_to_controller.emit(self.get_room_descriprion())
            self.model_signal_to_controller.emit(game_response)

            self.event_loop.exec()

    @pyqtSlot(str)
    def handle_inbound_signal(self, user_action):
        ''' Slot that receives a string from controller as a signal '''
        self.action = user_action
        self.event_loop.exit()


    def handle_outbound_signal(self, game_response):
        ''' Takes a string an send it to controller as a signal '''
        self.model_signal_to_controller.emit(game_response)

    def get_game_response(self):
        """ Takes a function and returns it as game_response """
        game_response = self.choose_action(self.action)
        return game_response
    
    
    def get_room_descriprion(self):
        """ Takes a function and returns its response """
        return(self.check_tile())


    def check_tile(self):
        self.room = world.tile_at(self.player.x, self.player.y)
        if self.player.is_alive():

            if self.player.verbose and self.room.enemy is None:
                return (f"\n***{self.room.name}***\n>{self.room.description}")
            
            elif (
                self.player.verbose
                and self.room.enemy.alive is True
                or not self.player.verbose
                and self.room.enemy is not None
                and self.room.enemy.alive is True
            ):
                return (f"{self.room.enemy.intro_alive}")
            elif self.player.verbose and self.room.enemy.alive is False:
                return (f"\n***{self.room.name}***\n>{self.room.enemy.intro_dead}")
            elif not self.player.verbose and self.room.enemy is None:
                return (f"\n***{self.room.name}***")
    
            
    def choose_action(self, action=str):
        if action in ["n", "s", "w", "e"]:
            if self.room.enemy is None or self.room.enemy.alive is False:
                self.move(self.room, self.player)
                return("You moved")
            else:
                return("You can't escape!")

        if action in ["diagnose"]:
            response = self.player.diagnose()
            return response
        
        elif action in ['now']:
            return (f"This room is {self.player.x}, {self.player.y}")


    def move(self, room, player):
        if self.action == "n" and world.tile_at(room.x, room.y - 1):
            player.move_north()
        elif self.action == "s" and world.tile_at(room.x, room.y + 1):
            player.move_south()
        elif self.action == "e" and world.tile_at(room.x + 1, room.y):
            player.move_east()
        elif self.action == "w" and world.tile_at(room.x - 1, room.y):
            player.move_west()
        else:
            pass



