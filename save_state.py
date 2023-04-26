import os, pickle

import world.tiles as world

def save(player):
    # Checks if the save files already exist and if so, delete them.
    if os.path.isfile('./saved_data.pkl'):
        os.remove("saved_data.pkl")
        print("Deleting old saved data...")

    player_data = {
        'name': player.name,
        'x': player.x,
        'y': player.y,
        'inventory': player.inventory,
        'level': player.lvl,
        'max_hp': player.max_hp,
        'hp': player.hp,
        'max_mana': player.max_mana,
        'mana': player.mana,
        'xp': player.xp,
        'xp_modifier': player.xp_modifier,
        'base_defence': player.base_defence,
        'current_weapon': player.current_weapon,
        'carryweight': player.carryweight,
        'gold': player.gold,
        'victory': player.victory,
        'previous_x': player.previous_x,
        'previous_y': player.previous_y,
        'turn': player.turn,
        'verbose': player.verbose,
        'bottle_full': player.bottle_full,

        'tavern_room_paid': player.tavern_room_paid,

        'ferns_talked': player.ferns_talked,
        'specimen_received' : player.specimen_received,
        'ferns_price_received' : player.ferns_price_received,

        'specimen_planted': player.specimen_planted,
        'oracle_response': player.oracle_response,

        'rina_gift_received': player.rina_gift_received
    }

    # Recreate a list of rooms with no gaps, updating it at the current state 
    player.rooms_list == []
    player.room_list_creator()

    # Creates lists of enemies, inventories, npcs and env objs on the map
    rooms_inventories = []
    world_enemies = []
    world_npcs = []
    world_env_objs = []
    for room in player.rooms_list:
        rooms_inventories.append(room.inventory)
        if room.enemy:
            world_enemies.append(room.enemy)
        if room.talker:
            world_npcs.append(room.talker)
        if room.env_obj:
            world_env_objs.append(room.env_obj)

    # Creates a list of all rooms with a chest
    chest_rooms = [room for room in player.rooms_list
                if isinstance(room, world.ChestTile)]

    # Saves all lists in the same file
    with open('saved_data.pkl', 'wb') as write:
        pickle.dump(player_data, write)
        pickle.dump(rooms_inventories, write)
        pickle.dump(world_enemies, write)
        pickle.dump(world_npcs, write)
        pickle.dump(world_env_objs, write)
        pickle.dump(chest_rooms, write)

def restore(player):
    # Restores all saved lists from the file (if it exists).
    # The names of the lists don't need to be the same as above, they are to facilitate reading
    if os.path.isfile('./saved_data.pkl'):
        with open('saved_data.pkl', 'rb') as read:
            player_data = pickle.load(read)
            rooms_inventories = pickle.load(read)
            world_enemies = pickle.load(read)
            world_npcs = pickle.load(read)
            world_env_objs = pickle.load(read)
            chest_rooms = pickle.load(read)
    else:
        print("There is no file to restore from!")
        return

    # PLAYER
    # Replaces player variables with saved ones
    player.name = player_data['name']
    player.x = player_data['x']
    player.y = player_data['y']
    player.inventory = player_data['inventory']
    player.lvl = player_data['level']
    player.max_hp = player_data['max_hp']
    player.hp = player_data['hp']
    player.max_mana = player_data['max_mana']
    player.mana = player_data['mana']
    player.xp = player_data['xp']
    player.xp_modifier = player_data['xp_modifier']
    player.current_weapon = player_data['current_weapon']
    player.carryweight = player_data['carryweight']
    player.gold = player_data['gold']
    player.victory = player_data['victory']
    player.previous_x = player_data['previous_x']
    player.previous_y = player_data['previous_y']
    player.turn = player_data['turn']
    player.verbose = player_data['verbose']
    player.bottle_full = player_data['bottle_full']

    player.tavern_room_paid = player_data['tavern_room_paid']

    player.ferns_talked = player_data['ferns_talked']
    player.specimen_received = player_data['specimen_received']
    player.ferns_price_received = player_data['ferns_price_received']

    player.specimen_planted = player_data['specimen_planted']
    player.oracle_response = player_data['oracle_response']

    player.rina_gift_received = player_data['rina_gift_received']

    # Check if a list of rooms with no gaps has already been created to avoid duplicates
    if player.rooms_list == []:
        player.room_list_creator()
    
    rooms_with_enemies = []
    rooms_with_npcs = []
    rooms_with_env_objs = []
    for i, room in enumerate(player.rooms_list, 0):
        # Replaces the room inventories with those saved in the file
        room.inventory = rooms_inventories[i]
        # Create a list of rooms on the map that currently have enemies
        if room.enemy:
            rooms_with_enemies.append(room)
        # Create a list of rooms on the map that currently have a npc
        if room.talker:
            rooms_with_npcs.append(room)
        # Create a list of rooms on the map that currently have env_objs
        if room.env_obj:
            rooms_with_env_objs.append(room)

    # Replaces the enemies in the above list with those saved in the file with attached updated status
    for i, room in enumerate(rooms_with_enemies, 0):
        room.enemy = world_enemies[i]

    # Replaces the inventory of npcs in the above list with the ones saved in the file
    for i, room in enumerate(rooms_with_npcs, 0):
        room.talker.inventory = world_npcs[i].inventory

    # Replaces the inventory of env_objs in the above list with the ones saved in the file
    for i, room in enumerate(rooms_with_env_objs):
        room.env_obj.inventory = world_env_objs[i].inventory

    # Create a list of rooms on the map that currently have a chest
    cur_chest_rooms = [room for room in player.rooms_list
                if isinstance(room, world.ChestTile)]
    # Changes the "closed" variable of the current room and makes it the same as that of the saved room
    for i, room in enumerate(cur_chest_rooms, 0):
        room.closed = chest_rooms[i].closed
