import os
import pickle

from world.map_tile import MapTile
from world.parser import WorldCreator


class GameState:
    def __init__(self):
        self.player_data = []
        self.world_copy = []
        self.list_with_all_rooms = []
        self.rooms_data = []


class Save(GameState):
    def __init__(self):
        super().__init__()

    def save_state(self, player):
        self.delete_old_save()
        self.player_data = player.get_player_data()
        self.world_copy = WorldCreator.world_map
        self.list_with_all_rooms = self.create_room_list()
        self.rooms_data = self.save_rooms_data()
        self.write_on_file()

    def delete_old_save(self):
        if os.path.isfile('saved_data.pkl'):
            os.remove("saved_data.pkl")
            print("> Deleting old saved data...")

    def write_on_file(self):
        with open('saved_data.pkl', 'wb') as write:
            pickle.dump(self.player_data, write)
            pickle.dump(self.world_copy, write)
            pickle.dump(self.list_with_all_rooms, write)
            pickle.dump(self.rooms_data, write)


class Reload(GameState):
    def __init__(self):
        super().__init__()

    def read_from_file(self):
        with open('saved_data.pkl', 'rb') as read:
            self.player_data = pickle.load(read)
            self.world_copy = pickle.load(read)
            self.list_with_all_rooms = pickle.load(read)
            self.rooms_data = pickle.load(read)

    def load_state(self, player):
        self.read_from_file()
        self.override_player_data(player)
        self.override_rooms_data()

    def check_if_file_exists(self):
        return bool(os.path.isfile('./saved_data.pkl'))

    def override_player_data(self, player):
        for attr, value in zip(vars(player), self.player_data):
            setattr(player, attr, value)

    def override_rooms_data(self):
        return WorldCreator.set_world_map(self.world_copy)
