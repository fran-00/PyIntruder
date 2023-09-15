from PyQt6.QtWidgets import QHBoxLayout, QPushButton

class GameButtons:
    def __init__(self, game_view):
        self.game_view = game_view
    
    def on_movements_buttons(self):
        """Add buttons for cardinal directions to game GUI"""
        button_north = QPushButton("🡅")
        button_south = QPushButton("🡇")
        button_east = QPushButton("🡆")
        button_west = QPushButton("🡄")

        buttons = [button_north, button_south, button_east, button_west]
        self.assign_css_class(buttons, "cardinal_directions")

        # Connect direction buttons to a common handler
        button_north.clicked.connect(lambda: self.game_view.handle_user_action("n"))
        button_south.clicked.connect(lambda: self.game_view.handle_user_action("s"))
        button_east.clicked.connect(lambda: self.game_view.handle_user_action("e"))
        button_west.clicked.connect(lambda: self.game_view.handle_user_action("w"))

        # Horizontal layout for direction buttons
        direction_layout = QHBoxLayout()
        direction_layout.addWidget(button_north)
        direction_layout.addWidget(button_south)
        direction_layout.addWidget(button_east)
        direction_layout.addWidget(button_west)
        
        return direction_layout
    
    def add_button(self, text, command, layout, buttons_list):
        button = QPushButton(text)
        button.clicked.connect(lambda: self.game_view.handle_user_action(command))
        layout.addWidget(button)
        buttons_list.append(button)
    
    def on_actions_buttons(self):
        """Add buttons for actions to game GUI"""
        button_attack = QPushButton("Attack")
        button_curse = QPushButton("Cast Curse")
        button_inventory = QPushButton("Inventory")
        button_diagnose = QPushButton("Diagnose")

        buttons = [button_attack, button_curse, button_inventory, button_diagnose]
        self.assign_css_class(buttons, "player_commands")

        button_attack.clicked.connect(lambda: self.game_view.handle_user_action("a"))
        button_curse.clicked.connect(lambda: self.game_view.handle_user_action("c"))
        button_inventory.clicked.connect(lambda: self.game_view.handle_user_action("i"))
        button_diagnose.clicked.connect(lambda: self.game_view.handle_user_action("diagnose"))

        command_layout = QHBoxLayout()
        command_layout.addWidget(button_attack)
        command_layout.addWidget(button_curse)
        command_layout.addWidget(button_inventory)
        command_layout.addWidget(button_diagnose)
        
        return command_layout
    
    def assign_css_class(self, buttons_list, class_name):
        for button in buttons_list:
            button.setProperty("class", class_name)
