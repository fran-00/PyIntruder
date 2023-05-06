from PyQt6.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, QEventLoop

import world.parser as parser
from .commands import Commands


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
        """Starts the game loop and handles player actions.

        Returns:
            None

        """
        self.commands = Commands(self.player, self.room)
        self.model_signal_to_controller.emit("******* PYINTRUDER*******")
        self.model_signal_to_controller.emit(self.commands.get_room_description())
        
        self.event_loop = QEventLoop()

        while True:
            self.room = parser.tile_at(self.player.x, self.player.y)
            if self.room.enemy and self.room.enemy.is_alive():
                self.handle_enemy_attack()

            self.event_loop.exec()
            game_response = self.commands.choose_action(self.action)

            if isinstance(game_response, tuple):
                self.process_nested_loop(game_response)
            else:
                self.model_signal_to_controller.emit(game_response)

    def process_nested_loop(self, game_response):
        for i, method in enumerate(game_response):
            self.commands.arguments_list.append(self.action)
            arguments_tuple = tuple(self.commands.arguments_list)
            nested_response = method(*arguments_tuple)
            
            if isinstance(nested_response, tuple) and nested_response[1] == None:
                self.model_signal_to_controller.emit(nested_response[0])
                break
            else:
                self.model_signal_to_controller.emit(nested_response)
                if i == len(game_response) - 1:
                    break
                else:
                    self.event_loop.exec()

    @pyqtSlot(str)
    def handle_inbound_signal(self, user_action):
        """
        Receives a string signal from the controller and sets the user action.

        This method is a slot that receives a string signal from the controller, which represents
        the user's chosen action. This slot sets the received string to the `action` instance variable
        and exits the event loop to continue the game execution.

        Args:
            user_action (str): A string representing the user action.

        """
        self.action = user_action.lower()
        self.event_loop.exit()

    def handle_outbound_signal(self, game_response):
        """Sends the given `game_response` string to the controller as a signal.

        Args:
            game_response: A string representing the game response to be sent.

        """
        self.model_signal_to_controller.emit(game_response)

    def handle_enemy_attack(self):
        """Handle an enemy attack on the player.

        This method calls the `modify_player` method of the `room` object to calculate the enemy attacks on the player.
        The resulting `enemy_attacks` are emitted to the controller using the `model_signal_to_controller` signal.

        """
        enemy_attacks = self.room.modify_player(self.player)
        self.model_signal_to_controller.emit(enemy_attacks)

