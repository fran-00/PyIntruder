import os
import pickle

from pyintruder.world.parser import WorldCreator


class GameState:
    def __init__(self):
        self.player_data = []
        self.world_copy = []


class Save(GameState):
    def __init__(self):
        super().__init__()

    def save_state(self, player):
        self.delete_old_save()
        self.player_data = player.get_player_data()
        self.world_copy = WorldCreator.world_map
        self.write_on_file()

    def delete_old_save(self):
        if os.path.isfile('saved_data.pkl'):
            os.remove("saved_data.pkl")

    def write_on_file(self):
        with open('saved_data.pkl', 'wb') as write:
            pickle.dump(self.player_data, write)
            pickle.dump(self.world_copy, write)


class Reload(GameState):
    def __init__(self):
        super().__init__()

    def read_from_file(self):
        with open('saved_data.pkl', 'rb') as read:
            self.player_data = pickle.load(read)
            self.world_copy = pickle.load(read)

    def load_state(self, player):
        self.read_from_file()
        self.overwrite_player_data(player)
        self.overwrite_world_data()

    def check_if_file_exists(self):
        return bool(os.path.isfile('./saved_data.pkl'))

    def overwrite_player_data(self, player):
        for attr, value in zip(vars(player), self.player_data):
            setattr(player, attr, value)

    def overwrite_world_data(self):
        return WorldCreator.set_world_map(self.world_copy)
