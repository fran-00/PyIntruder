class GameGUI:
    def __init__(self, game_view):
        self.game_view = game_view

    def assign_css_class(self, gui_elements, class_name):
        for element in gui_elements:
            element.setProperty("class", class_name)
