from PyQt6.QtWidgets import QHBoxLayout, QPushButton

class GameButtons:
    def __init__(self, game_view):
        self.game_view = game_view
    
    def on_movements_buttons(self):
        """Add buttons for cardinal directions to game GUI"""
        buttons = []
        directions_layout = QHBoxLayout()

        self.add_button("🡅", "n", directions_layout, buttons)
        self.add_button("🡇", "s", directions_layout, buttons)
        self.add_button("🡆", "e", directions_layout, buttons)
        self.add_button("🡄", "w", directions_layout, buttons)

        self.assign_css_class(buttons, "cardinal_directions")

        return directions_layout
    
    def on_actions_buttons(self):
        """Add buttons for actions to game GUI"""
        buttons = []
        actions_layout = QHBoxLayout()

        self.add_button("Attack", "a", actions_layout, buttons)
        self.add_button("Cast Curse", "c", actions_layout, buttons)
        self.add_button("Inventory", "i", actions_layout, buttons)
        self.add_button("Diagnose", "diagnose", actions_layout, buttons)

        self.assign_css_class(buttons, "action_buttons")

        return actions_layout

    def add_button(self, text, command, layout, buttons_list):
        button = QPushButton(text)
        button.clicked.connect(lambda: self.game_view.handle_user_action(command))
        layout.addWidget(button)
        buttons_list.append(button)

    def assign_css_class(self, buttons_list, class_name):
        for button in buttons_list:
            button.setProperty("class", class_name)
