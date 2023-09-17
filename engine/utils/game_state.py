import os
import pickle

from world.map_tile import MapTile
from world.tiles import ChestTile
from world.parser import get_world_map



class Save:
    def __init__(self, player):
        self.player = player
        self.player_data = []
        self.rooms_list = []
        self.rooms_inventories = []
        self.world_enemies = []
        self.world_npcs = []
        self.world_env_objs = []
        self.world_npcs = []
    
    def save_state(self, player):
        self.delete_old_save()
        self.player_data = player.get_player_data()
        self.create_room_list()
        self.split_room_list()
        self.write_on_file()

    def delete_old_save(self):
        if os.path.isfile('saved_data.pkl'):
            os.remove("saved_data.pkl")
            print("> Deleting old saved data...")

    def create_room_list(self):
        rooms_list_with_empty_spaces = []
        tiles = get_world_map()
        for tile in tiles:
            rooms_list_with_empty_spaces.extend(tile)
        return [
            room
            for room in rooms_list_with_empty_spaces
            if isinstance(room, MapTile)
        ]

    def split_room_list(self):
        for room in self.rooms_list:
            self.rooms_inventories.append(room.inventory)
            if room.enemy:
                self.world_enemies.append(room.enemy)
            if room.talker:
                self.world_npcs.append(room.talker)
            if room.env_obj:
                self.world_env_objs.append(room.env_obj)
            self.chest_rooms = [room for room in self.rooms_list
                   if isinstance(room, ChestTile)]

    def write_on_file(self):
        with open('saved_data.pkl', 'wb') as write:
            pickle.dump(self.player_data, write)
            pickle.dump(self.rooms_inventories, write)
            pickle.dump(self.world_enemies, write)
            pickle.dump(self.world_npcs, write)
            pickle.dump(self.world_env_objs, write)
            pickle.dump(self.chest_rooms, write)