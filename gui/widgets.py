from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit

from .game_gui import GameGUI


class GameButtons(GameGUI):
    def __init__(self, game_view):
        super().__init__(game_view)

    def on_parent_buttons_layout(self):
        buttons_parent_layout = QHBoxLayout(objectName="buttons_parent_layout")
        buttons_parent_layout.addLayout(self.on_movements_buttons())
        buttons_parent_layout.addLayout(self.on_actions_buttons())
        return buttons_parent_layout
    
    def on_movements_buttons(self):
        """Add buttons for cardinal directions to game GUI"""
        buttons = []
        inactive_buttons = []
        directions_layout = QVBoxLayout(objectName="directions_layout")

        upper_container = QHBoxLayout()
        middle_container = QHBoxLayout()
        lower_container = QHBoxLayout()

        self.add_inactive_button("  ", upper_container, inactive_buttons)
        self.add_button("🡅", "go north", upper_container, buttons)
        self.add_inactive_button("  ", upper_container, inactive_buttons)
        self.add_button("🡄", "go west", middle_container, buttons)
        self.add_inactive_button("  ", middle_container, inactive_buttons)
        self.add_button("🡆", "go east", middle_container, buttons)
        self.add_inactive_button("  ", lower_container, inactive_buttons)
        self.add_button("🡇", "go south", lower_container, buttons)
        self.add_inactive_button("  ", lower_container, inactive_buttons)

        directions_layout.addLayout(upper_container)
        directions_layout.addLayout(middle_container)
        directions_layout.addLayout(lower_container)

        self.assign_css_class(buttons, "cardinal_directions")
        self.assign_css_class(inactive_buttons, "inactive_buttons")

        return directions_layout
    
    def on_actions_buttons(self):
        """Add buttons for actions to game GUI"""
        buttons = []
        actions_parent_layout = QVBoxLayout(objectName="actions_parent_layout")

        self.add_button("Attack", "attack", actions_parent_layout, buttons)
        self.add_button("Cast Curse", "curse", actions_parent_layout, buttons)
        self.add_button("Inventory", "inventory", actions_parent_layout, buttons)
        self.add_button("Diagnose", "diagnose", actions_parent_layout, buttons)

        self.assign_css_class(buttons, "action_buttons")

        return actions_parent_layout

    def add_button(self, text, command, layout, buttons_list):
        button = QPushButton(text)
        button.clicked.connect(lambda: self.game_view.handle_user_action(command))
        layout.addWidget(button)
        buttons_list.append(button)

    def add_inactive_button(self, text, layout, buttons_list):
        button = QPushButton(text)
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
        send_button = QPushButton("Enter", objectName="enter_button")
        # send_button.setObjectName("enter_button")
        send_button.clicked.connect(lambda: self.game_view.handle_user_action("none"))

        # Horizontal layout for input box and button
        input_layout = QHBoxLayout(objectName="input_layout")
        input_layout.addWidget(self.game_view.input_box)
        input_layout.addWidget(send_button)

        return input_layout
