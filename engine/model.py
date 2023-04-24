from PyQt6.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, QEventLoop

import old_world_gen as world


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
        self.room = world.tile_at(self.player.x, self.player.y)
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
            if self.room.enemy and self.room.enemy.alive:
                self.handle_enemy_attack()
            
            self.player.turn += 1
            self.event_loop.exec()
            
            game_response = self.choose_action(self.action)
            self.model_signal_to_controller.emit(game_response)
            
            if game_response == self.player.show_inventory():
                self.event_loop.exec()
                inventory_response = self.player.choose_item(self.action)
                self.model_signal_to_controller.emit(inventory_response)
    
    
    @pyqtSlot(str)
    def handle_inbound_signal(self, user_action):
        ''' Slot that receives a string from controller as a signal '''
        self.action = user_action
        self.event_loop.exit()


    def handle_outbound_signal(self, game_response):
        ''' Takes a string an send it to controller as a signal '''
        self.model_signal_to_controller.emit(game_response)

    
    def handle_enemy_attack(self):
        enemy_attacks = self.room.modify_player(self.player)
        self.model_signal_to_controller.emit(enemy_attacks)


    def get_room_description(self):
        self.room = world.tile_at(self.player.x, self.player.y)
        if self.room.enemy is None:
            return (f"\n***{self.room.name}***\n> {self.room.description}")
        elif self.room.enemy.alive:
            return (f"{self.room.enemy.intro_alive}")
        elif self.player.verbose and self.room.enemy.alive is False:
            return (f"\n***{self.room.name}***\n>{self.room.enemy.intro_dead}")
        elif not self.player.verbose and self.room.enemy is None:
            return (f"\n***{self.room.name}***")
    
            
    def choose_action(self, action=str):
        if action in ["n", "s", "w", "e"]:
            if self.room.enemy is None or self.room.enemy.alive is False:
                return(self.move(self.room, self.player))
            else:
                return("You can't escape!")

        elif action in ["diagnose"]:
            response = self.player.diagnose()
            return response
        
        elif action in ['now']:
            return (f"This room is {self.player.x}, {self.player.y}")
        
        elif action in ["i"]:
            response = self.player.show_inventory()
            return response
        
        elif action in ["a"]:
            if self.room.enemy and self.room.enemy.alive:
                response = self.player.attack()
            else:
                response = "There is no one to attack here!"
            return response
        
        else:
            return ("I beg your pardon?")


    def move(self, room, player):
        if self.action == "n" and world.tile_at(room.x, room.y - 1):
            player.move_north()
        elif self.action == "s" and world.tile_at(room.x, room.y + 1):
            player.move_south()
        elif self.action == "e" and world.tile_at(room.x + 1, room.y):
            player.move_east()
        elif self.action == "w" and world.tile_at(room.x - 1, room.y):
            player.move_west()
        return(self.get_room_description())



