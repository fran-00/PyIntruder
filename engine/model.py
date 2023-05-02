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
        self.arguments_list = []
        super().__init__()

    def play(self):
        """Starts the game loop and handles player actions.

        Returns:
            None

        """
        self.event_loop = QEventLoop()

        while True:
            if self.room.enemy and self.room.enemy.alive:
                self.handle_enemy_attack()

            self.event_loop.exec()
            game_response = self.choose_action(self.action)

            if isinstance(game_response, tuple):
                self.process_nested_loop(game_response)
            else:
                self.model_signal_to_controller.emit(game_response)

    def process_nested_loop(self, game_response):
        for i, method in enumerate(game_response):
            self.arguments_list.append(self.action)
            arguments_tuple = tuple(self.arguments_list)
            nested_response = method(*arguments_tuple)
            self.model_signal_to_controller.emit(nested_response)
            if nested_response in [None, "Invalid choice, try again."] or i == len(game_response) - 1:
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
        self.action = user_action
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

    def get_room_description(self):
        self.room = parser.tile_at(self.player.x, self.player.y)
        if self.room.enemy is None:
            return (f"***{self.room.name}***\n> {self.room.description}")
        elif self.room.enemy.alive:
            return (f"{self.room.enemy.description}")

    def choose_action(self, action=str):
        """Chooses an action based on the given input string and returns its result.

        Args:
            action (str): The input string representing the action to be taken.

        Returns:
            # TODO

        """
        self.player.turn += 1
        if action in ["n", "s", "w", "e"]:
            if self.room.enemy is None or self.room.enemy.alive is False:
                return (self.move(self.room, self.player))
            else:
                return ("You can't escape!")

        elif action in ["diagnose"]:
            return self.player.diagnose()

        elif action in ['now']:
            return (f"This room is {self.player.x}, {self.player.y}")

        elif action in ["i"]:
            self.arguments_list = [self.player.inventory, "my-inventory"]
            return (
                self.player.show_inventory,
                self.player.choose_item
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

        elif action in ["trade"]:
            if self.room.talker and self.room.talker.trade:
                self.arguments_list = [self.room.talker.inventory, "trade"]
                self.model_signal_to_controller.emit(self.room.talker.hello)

                return (
                    self.player.choose_nested_action,
                    self.player.trading_mode,
                    self.player.choose_item,
                )
            elif self.room.talker and not self.room.talker.trade:
                return f" {self.room.talker.name} doesn't want to trade"
            else:
                return "There is no one to trade with!"

        elif action in ["p", "pick up"]:
            if self.room.inventory:
                self.arguments_list = [self.room.inventory, "pick-up"]
                self.model_signal_to_controller.emit("What do you want to pick up?")
                return (
                    self.player.show_inventory,
                    self.player.choose_item
                )
        
        elif action in ["d", "drop"]:
            if self.player.inventory:
                self.arguments_list = [self.player.inventory, "drop"]
                self.model_signal_to_controller.emit("What do you want to drop?")
                return (
                    self.player.show_inventory,
                    self.player.choose_item
                )
            else:
                return "Your inventory is empty."

        elif action in ["m", "map"]:
            return self.player.show_map()

        else:
            return ("I beg your pardon?")

    def move(self, room, player):
        """Move the player in the specified direction if possible and return the room description.

        Args:
            room (Room(MapTile)): The current room from world.tiles
            player (Player): The player object.

        Returns:
            str: Room's description if player is able to move, or an error message if the requested direction is not valid.

        """
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
        return (self.get_room_description())
