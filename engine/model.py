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
        """Starts the game loop and handles player actions.

        The method starts an event loop to handle user actions and game events. It continuously checks
        if there is an enemy in the room and if it is alive, then handles the enemy attack. It waits for
        the user to choose an action and executes it. If the action returns a tuple, the method creates
        a nested loop to handle the second method passed in the tuple and emits the result to the controller.

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
            Union[str, Tuple[Any, Callable, List, bool]]: The actual return 
            value and its format depend on the chosen action: it can a string 
            or a tuple containing arguments that must be passed to Player's methods

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
            return (
                self.player.show_inventory(self.player.inventory, False),
                self.player.choose_item,
                self.player.inventory,
                False,
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
            if self.room.talker:
                return (
                    self.player.show_inventory(
                        self.room.talker.inventory, True),
                    self.player.choose_item,
                    self.room.talker.inventory,
                    True
                )
            else:
                return "There is no one to trade with!"

        elif action in ["p", "pick up"]:
            return self.player.item_handler()

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
