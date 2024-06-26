from PyQt6.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, QEventLoop

from pyintruder.world.parser import WorldCreator
from .utils.commands import Commands
from .utils.combat_system import Combat


class GameThread(QThread):
    def __init__(self, game_model):
        super().__init__()
        self.game_model = game_model

    def run(self):
        self.game_model.play()


class GameModel(QObject):
    model_signal_to_controller = pyqtSignal(str)
    player_status_signal = pyqtSignal(tuple)

    def __init__(self, player):
        self.player = player
        self.action = None
        self.room = None
        super().__init__()

    def play(self):
        """
        TODO: UPDATE DOCSTRING
        Start game loop and allow user to move and perform actions within a
        grid-based map connecting player, game world and all game features
        through Commands class.

        Start game loop, check if there's a living enemy in the current room
        and if so call process_enemy_attack method from MapTile class.
        Then allow user to choose an action, passing the signal received from
        GameController as argument to choose_action method from Command class.
        The result of this operation may be a string or a tuple.
        If it is a string, it is emitted as a signal to Controller.
        if it is a tuple, it means that several methods of Player class must be 
        executed in sequence and that loop must be broken when required to allow
        the user to make a choice.
        In this case, the tuple is passed as argument of process_nested_loop
        method, that will handle nested loop.

        Returns
        -------
        None
            Send game output as signals to the GameController class.
        """
        self.commands = Commands(self.player, self.room)
        self.model_signal_to_controller.emit("<h1>PYINTRUDER</h1>")
        self.model_signal_to_controller.emit(self.commands.get_room_description())
        self.event_loop = QEventLoop()

        while True:
            self.process_main_loop()

    def process_main_loop(self):
        """
        TODO: Update docstring after methods extraction.

        Process a tuple of methods in a for loop.

        First add action to be processed to argument_list attribute of Commands
        class (a list of arguments to be passed to the methods processed in the loop
        and which depend on the command sent by the user) and convert this list 
        into a tuple. Then pass the tuple as an argument to the current method
        that loop is processing.
        If this operation results in another tuple that has None as the second 
        element, emit the first element as a signal and interrupt the loop: this
        means that an exception was raised or the user canceled the operation.
        Otherwise resume loop execution to be able to receive the user's input
        and process it in the next iteration.

        Parameters
        ----------
        game_response : tuple
            Tuple of methods to be processed in the nested loop.

        Returns
        -------
        None
            Emit PyQT signal to Controller for each nested response processed.
        """
        self.room = WorldCreator.tile_at(self.player.x, self.player.y)
        if self.room.enemy and self.room.enemy.is_alive():
            self.process_enemy_attack()

        self.handle_player_status_signal(
            self.player.hp,
            self.player.max_hp,
            self.player.mana,
            self.player.max_mana
        )

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

            if isinstance(nested_response, tuple):
                self.model_signal_to_controller.emit(nested_response[0])
                if nested_response[1] is None:
                    break
                elif nested_response[1] == "dialogue":
                    self.process_dialogue(nested_response)

            else:
                self.model_signal_to_controller.emit(nested_response)
                if i == len(game_response) - 1:
                    break
                else:
                    self.event_loop.exec()

    def process_dialogue(self, nested_response):
        # TODO: Add a way to process dialogues with npcs
        self.commands.arguments_list.append(nested_response[2])
        self.commands.arguments_list.append(nested_response[3])
        self.event_loop.exec()

    def process_enemy_attack(self):
        """Handle an enemy attack on the player.

        Call the `modify_player` method from MapTile class to calculate enemy
        attacks on the player. The resulting `enemy_attacks` are emitted to
        GameController using the `model_signal_to_controller` signal.
        """
        if self.player.is_alive():
            enemy_attacks = Combat.modify_player(self.room, self.player)
            self.model_signal_to_controller.emit(enemy_attacks)
        else:
            self.model_signal_to_controller.emit(
                "You can start a New Game, Reload from file (if any) or Quit.")

    @pyqtSlot(str)
    def handle_inbound_signal(self, user_action):
        """
        Receive a string signal and set user action.

        This is a slot that receives a string signal from GameController class
        which represents user's chosen action.
        Set received string to `action` instance variable and exit event loop 
        to continue game execution.

        Parameters
        ----------
        user_action : str
            A string representing the user action.
        """
        self.action = user_action.lower()
        self.event_loop.exit()

    def handle_outbound_signal(self, game_response):
        """Send given `game_response` string to GameController as a signal.

        Parameters
        ----------
            game_response : str
                A string representing the game response to be sent.
        """
        self.model_signal_to_controller.emit(game_response)

    def handle_player_status_signal(self, player_hp, player_max_hp, player_mana, player_max_mana):
        """
        """
        player_data = player_hp, player_max_hp, player_mana, player_max_mana
        self.player_status_signal.emit(player_data)
