from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit

from .game_gui import GameGUI


class GameButtons(GameGUI):
    def __init__(self, game_view):
        super().__init__(game_view)

    def on_parent_buttons_layout(self):
        parent_layout = QHBoxLayout()
        parent_layout.addLayout(self.on_movements_buttons())
        parent_layout.addLayout(self.on_actions_buttons())
        return parent_layout
    
    def on_movements_buttons(self):
        """Add buttons for cardinal directions to game GUI"""
        buttons = []
        directions_layout = QHBoxLayout()

        self.add_button("🡅", "go north", directions_layout, buttons)
        self.add_button("🡇", "go south", directions_layout, buttons)
        self.add_button("🡆", "go east", directions_layout, buttons)
        self.add_button("🡄", "go west", directions_layout, buttons)

        self.assign_css_class(buttons, "cardinal_directions")

        return directions_layout
    
    def on_actions_buttons(self):
        """Add buttons for actions to game GUI"""
        buttons = []
        actions_layout = QHBoxLayout()

        self.add_button("Attack", "attack", actions_layout, buttons)
        self.add_button("Cast Curse", "curse", actions_layout, buttons)
        self.add_button("Inventory", "inventory", actions_layout, buttons)
        self.add_button("Diagnose", "diagnose", actions_layout, buttons)

        self.assign_css_class(buttons, "action_buttons")

        return actions_layout

    def add_button(self, text, command, layout, buttons_list):
        button = QPushButton(text)
        button.clicked.connect(lambda: self.game_view.handle_user_action(command))
        layout.addWidget(button)
        buttons_list.append(button)


class GameEntry(GameGUI):
    def __init__(self, game_view):
        super().__init__(game_view)

    def on_input_layout(self):
        """Add horizzontal input box and a send button to submit"""
        self.game_view.input_box = QLineEdit()
        self.game_view.input_box.returnPressed.connect(lambda: self.game_view.handle_user_action("none"))

        # Button to submit input
        send_button = QPushButton("Enter")
        send_button.setProperty("class", "enter_button")
        send_button.clicked.connect(lambda: self.game_view.handle_user_action("none"))

        # Horizontal layout for input box and button
        input_layout = QHBoxLayout()
        input_layout.setProperty("class", "input_layout")
        input_layout.addWidget(self.game_view.input_box)
        input_layout.addWidget(send_button)

        return input_layout
