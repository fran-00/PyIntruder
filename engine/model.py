from PyQt6.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, QEventLoop

from entities.entities_templates import Armor
import world.parser as parser


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
        self.room = parser.tile_at(self.player.x, self.player.y)
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
            
            self.event_loop.exec()
            game_response = self.choose_action(self.action)
            
            # If game_response is a tuple creates a nested loop to handle the
            # second method passed and emits the result.
            if isinstance(game_response, tuple):
                self.model_signal_to_controller.emit(game_response[0])
                self.event_loop.exec()
                method, *args = game_response[1:]
                
                if args:
                    nested_response = method(self.action, *args)
                else:
                    nested_response = method(self.action)
                
                self.model_signal_to_controller.emit(nested_response)
            else:
                self.model_signal_to_controller.emit(game_response)

    
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
        self.room = parser.tile_at(self.player.x, self.player.y)
        if self.room.enemy is None:
            return (f"\n***{self.room.name}***\n> {self.room.description}")
        elif self.room.enemy.alive:
            return (f"{self.room.enemy.description}")
        elif self.player.verbose and self.room.enemy.alive is False:
            # TODO: if enemy is dead, it must show a message that depends on enemy
            return (f"\n***{self.room.name}***\n>{self.room.enemy.name} is dead.")
        elif not self.player.verbose and self.room.enemy is None:
            return (f"\n***{self.room.name}***")
    
            
    def choose_action(self, action=str):
        self.player.turn += 1
        if action in ["n", "s", "w", "e"]:
            if self.room.enemy is None or self.room.enemy.alive is False:
                return(self.move(self.room, self.player))
            else:
                return("You can't escape!")

        elif action in ["diagnose"]:
            return self.player.diagnose()
        
        elif action in ['now']:
            return (f"This room is {self.player.x}, {self.player.y}")
        
        elif action in ["i"]:
            return (
                self.player.show_inventory(self.player.inventory, None), 
                self.player.choose_item, 
                None, 
                self.player.inventory
            )
        
        elif action in ["a"]:
            if self.room.enemy and self.room.enemy.alive:
                return self.player.attack()
            else:
                return "There is no one to attack here!"
        
        elif action in ["c"]:
            if self.room.enemy and self.room.enemy.alive:
                return self.player.cast_curse()
            else:
                return "There is no one to curse here!"

        elif action in ["t", "talk"]:
            return self.room.dialogue()
        
        elif action in ["p", "pick up"]:
            return self.player.item_handler()

        elif action in ["m", "map"]:
            return self.player.show_map()
        
        else:
            return ("I beg your pardon?")


    def move(self, room, player):
        if self.action == "n" and parser.tile_at(room.x, room.y - 1):
            player.move_north()
        elif self.action == "s" and parser.tile_at(room.x, room.y + 1):
            player.move_south()
        elif self.action == "e" and parser.tile_at(room.x + 1, room.y):
            player.move_east()
        elif self.action == "w" and parser.tile_at(room.x - 1, room.y):
            player.move_west()
        else:
            return "You can't go that way!"
        return(self.get_room_description())



