import os
import pickle

from world.map_tile import MapTile
from world.tiles import ChestTile
from world.parser import get_world_map



class Save:
    def __init__(self):
        self.player_data = []
        self.rooms_list = []
        self.rooms_inventories = []
        self.rooms_enemies = []
        self.rooms_npcs = []
    
    def save_state(self, player):
        self.delete_old_save()
        self.player_data = player.get_player_data()
        self.room_list = self.create_room_list()
        self.save_rooms_inventories()
        self.save_rooms_enemies()
        self.save_rooms_npcs()
        self.write_on_file()

    def delete_old_save(self):
        if os.path.isfile('saved_data.pkl'):
            os.remove("saved_data.pkl")
            print("> Deleting old saved data...")

    def create_room_list(self):
        rooms_list_with_nested_lists = []
        tiles = get_world_map()
        for tile in tiles:
            rooms_list_with_nested_lists.extend(tile)
        return [
            room
            for room in rooms_list_with_nested_lists
            if isinstance(room, MapTile)
        ]

    # def save_rooms_inventories(self):
    #     return [room.inventory for room in self.rooms_list]
    def save_rooms_inventories(self):
        for room in self.room_list:
            self.rooms_inventories.append(room.inventory)

    def save_rooms_enemies(self):
        for room in self.room_list:
            if room.enemy:
                self.rooms_enemies.append(room.enemy)

    def save_rooms_npcs(self):
        for room in self.room_list:
            if room.enemy:
                self.rooms_npcs.append(room.talker)

    def write_on_file(self):
        with open('saved_data.pkl', 'wb') as write:
            pickle.dump(self.player_data, write)
            pickle.dump(self.rooms_inventories, write)
            pickle.dump(self.rooms_enemies, write)
            pickle.dump(self.rooms_npcs, write)


class Reload:
    def __init__(self):
        self.player_data = []
        self.rooms_inventories = []
        self.world_enemies = []
        self.world_npcs = []

    def read_from_file(self):
        with open('saved_data.pkl', 'rb') as read:
            self.player_data = pickle.load(read)
            self.rooms_inventories = pickle.load(read)
            self.world_enemies = pickle.load(read)
            self.world_npcs = pickle.load(read)
    
    def check_if_file_exists(self):
        return bool(os.path.isfile('./saved_data.pkl'))

    def load_player_data(self, player):
        pass

    def load_state(self):
        pass
