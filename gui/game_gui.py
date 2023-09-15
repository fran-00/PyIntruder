class GameGUI:
    def __init__(self, game_view):
        self.game_view = game_view

    def assign_css_class(self, buttons_list, class_name):
        for button in buttons_list:
            button.setProperty("class", class_name)