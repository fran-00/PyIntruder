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
            game_response = self.get_game_response()
            print(f"MODEL: Game response is: {game_response}")
            
            # self.model_signal_to_controller.emit(self.get_room_descriprion(logic))
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
    
    
    def get_room_descriprion(self, logic):
        """ Takes a function and returns its response """
        return(self.check_tile())


    def check_tile(self):
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
        available_actions = self.get_available_actions(self.room, self.player)
        # FIXME:
        # action = available_actions.get(action)

        if action in ["diagnose"]:
            response = self.player.diagnose()
            return response
        
        elif action in ['now']:
            return (f"This room is {self.player.x}, {self.player.y}")

        # *** FORBIDDEN DIRECTIONS ***
        elif (available_actions != ['n', 's', 'w', 'e'] and
            action in ['n', 's', 'w', 'e'] and
            self.room.enemy is not None and self.room.enemy.alive is True):
            return ("You cannot leave while an enemy attacks you!")

        elif available_actions != 'n' and action in ['n']:
            if self.room.enemy is None or self.room.enemy.alive is False:
                return ("You can't go north from here.")

        elif available_actions != 's' and action in ['s']:
            if self.room.enemy is None or self.room.enemy.alive is False:
                return ("You can't go south from here.")

        elif available_actions != 'w' and action in ['w']:
            if self.room.enemy is None or self.room.enemy.alive is False:
                return ("You can't go west from here.")

        elif available_actions != 'e' and action in ['e']:
            if self.room.enemy is None or self.room.enemy.alive is False:
                return ("You can't go east from here.")

        elif available_actions != 'h' and action in ['h']:
            return ("Your health is already full.")

        elif available_actions != 'a' and action in ['a']:
            return ("There is no one to attack here.")

        elif available_actions != 'c' and action in ['c']:
            return ("There is no one to curse here.")

        else:
            return("I beg you pardon?")


    def get_available_actions(self, room, player):
        actions = OrderedDict()

        if room.enemy is None or room.enemy.alive is False:
            self.available_directions(room, actions, player)
        if room.enemy is not None and room.enemy.alive is True:
            self.action_adder(actions, 'a', player.attack, "attack")
        if room.enemy is not None and room.enemy.alive is True:
            self.action_adder(actions, 'c', player.cast_curse, "cast curse")
        if room.enemy is not None and room.enemy.alive is True:
            self.action_adder(actions, 'r', player.run, "run")
        if room.talker:
            self.action_adder(actions, 't', player.check_dialogue, "talk")
        if player.hp < player.max_hp:
            self.action_adder(actions, 'h', player.heal, "heal")
        return actions


    def available_directions(self, room, actions, player):
        if world.tile_at(room.x, room.y - 1):
            self.action_adder(actions, 'n', player.move_north, "north")
        if world.tile_at(room.x, room.y + 1):
            self.action_adder(actions, 's', player.move_south, "south")
        if world.tile_at(room.x + 1, room.y):
            self.action_adder(actions, 'e', player.move_east, "east")
        if world.tile_at(room.x - 1, room.y):
            self.action_adder(actions, 'w', player.move_west, "west")


    def action_adder(self, action_dict, hotkey, action, name):
        action_dict[hotkey.lower()] = action
        action_dict[hotkey.upper()] = action
        print(f"| {hotkey}: {name}")

