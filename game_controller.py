class GameController:
    def __init__(self, view, game):
        self.view = view
        self.game = game
        self.view.input_submitted.connect(self.handle_input)

    def handle_input(self, user_input):
        response = self.game.choose_action(user_input)
        self.view.display_output(response)