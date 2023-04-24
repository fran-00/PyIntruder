import contextlib
import os
import pickle
import random

import old_world_gen as world
import old_entities_data.items as items
import entities.entities_index as entities_index


# MODULO DEL GIOCATORE
class Player:
    def __init__(self):
        self.name = 'Your Name Here'
        self.x = world.start_tile_location[0]       # modifica questi valori per modificare la locazione di partenza. di base è su (0, 1)
        self.y = world.start_tile_location[1]       # ma in realtà la locazione di partenza è determinata da dove metti la StartTile
        self.inventory = [items.Manuport()]
        self.lvl = 1
        self.max_hp = 100
        self.hp = 100
        self.max_mana = 100
        self.mana = 100
        self.xp = 0
        self.xp_modifier = 100
        self.base_defence = 0
        self.current_weapon = self.best_weapon()
        self.carryweight = 1
        self.gold = 10
        self.victory = False
        self.previous_x = None
        self.previous_y = None
        self.turn = 0
        self.verbose = True
        self.bottle_full = True
        self.rooms_list = []

        # GAME VARIABLES
        # Tavern
        self.tavern_room_paid = False

        # Ferns
        self.ferns_talked = False
        self.specimen_received = False
        self.ferns_price_received = False

        # Oak
        self.specimen_planted = False
        self.oracle_response = False

        # Rina
        self.rina_gift_received = False


    # *** MOVEMENT ***
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_north(self):
        self.get_coordinates(0, -1)

    def move_south(self):
        self.get_coordinates(0, 1)

    def move_east(self):
        self.get_coordinates(1, 0)

    def move_west(self):
        self.get_coordinates(-1, 0)

    def stand_still(self):
        self.get_coordinates(dx=0, dy=0)

    def get_coordinates(self, dx, dy):
        self.previous_x = self.x
        self.previous_y = self.y
        self.move(dx=dx, dy=dy)


    # *** ATTACK (WITH A WEAPON) ***
    def attack(self):
        best_weapon = self.best_weapon()
        room = world.tile_at(self.x, self.y)
        enemy = room.enemy
        response = ""

        if best_weapon is None:
            return "You don't have any weapon with you."
        
        if enemy is None or not enemy.alive:
            return

        response += f"You try to hit {enemy.name} with {best_weapon.name}!"
        precision = random.randint(1,20)

        if precision == 20:
            damage_multiplier = 2
            response += f"\nCritical hit! You deal {best_weapon.damage * damage_multiplier} DMG!"
        elif precision in [17, 18, 19]:
            damage_multiplier = 1.5
            response += f"\nGood hit! You deal {best_weapon.damage * damage_multiplier} DMG!"
        elif precision <= 3:
            response += "\nMissed!"
            return response
        else:
            damage_multiplier = 1
            response += f"\nYou deal {best_weapon.damage} DMG!"

        enemy.hp -= best_weapon.damage * damage_multiplier

        if enemy.hp <= 0:
            xp_earned = (room.enemy.hp // 2)
            self.xp += xp_earned
            response += f"\nYEAH! You killed that fucking bastard! You earned {xp_earned} XP!"

            loot = random.randint(10,200)
            self.level_up()
            self.gold += loot
            response += f"\nThe asshole lost his booty. Now {loot} Pine Cones are yours!"
            enemy.alive = False
        else:
            response += f"\n{enemy.name} has {enemy.hp} HP remaining."

        return response


    # *** BEST WEAPON ***
    def best_weapon(self):
        max_damage = 0
        best_weapon = None
        if weapons := [
            item for item in self.inventory if isinstance(item, items.Weapon)
        ]:
            for i, item in enumerate(weapons, 1):
                with contextlib.suppress(AttributeError):
                    if item.damage > max_damage:
                        best_weapon = item
                        max_damage = item.damage
            return best_weapon
        else:
            return None


    # *** INVENTORY ***
    def sort_items_by_category(self, category):
        return sorted([item for item in self.inventory if isinstance(item, category)], key=lambda item: item.name.lower())

    def show_inventory(self):
        response = "You open your backpack:"
        right_order_list = []
        index = 1
        for category in [items.Weapon, items.Curse, items.Consumable, items.ManaRechargers, items.Armor, items.MissionItem]:
            items_in_category = self.sort_items_by_category(category)
            if items_in_category:
                response += f"\n>> {category.__name__.upper()}:\n"
                for i, item in enumerate(items_in_category, index):
                    response += f"{index}. {item}"
                    index += 1
                    right_order_list.append(item)
        self.inventory = right_order_list
        response += f"\nYour wealth: {self.gold} §"
        response += "\nChoose a number to read an item's description or press Q to quit."
        return response

    def choose_item(self, action):
        if action.lower() in ('q', 'exit', 'no'):
            return "Ok."
        try:
            choice = int(action)-1
            to_read = self.inventory[choice]
            return f"{to_read.name}: {to_read.description}"
        except (ValueError, IndexError):
            return "Invalid choice, try again."


    # *** DIAGNOSE ***
    def diagnose(self):
        return (
            f"You have {self.hp}/{self.max_hp} HP and {self.mana}/{self.max_mana} Mana remaining. This is turn number {self.turn}."
        )


#TODO: All these methods need to be fixed
# Call TAVERN ROOM CLOSED**
    def tavern_room_closed(self):
        print("The room door is closed.")
        return

# CALL *** ALIVE ***
    def is_alive(self):
        return self.hp > 0

# CALL *** ARMOR ***
    def armor(self):
        armors = [item for item in self.inventory
                       if isinstance(item, items.Armor)]
        if not armors:
            print("You've got no armor.")
            return
        print("Choose an armor to wear:")
        for i, item in enumerate(armors, 1):
            print(f"{i}. {item}")

        valid = False
        while not valid:
            choice = input(">>>> ")
            try:
                armor_chosen = armors[int(choice) - 1]
                self.base_defence = armor_chosen.defence
                print(f"Your defence is now {self.base_defence}.")
                valid = True
            except (ValueError, IndexError):
                print("Invalid choice, try again.")
                return


# CALL *** CAST CURSE ***
    def cast_curse(self):
        while True:
            curses = [item for item in self.inventory
                       if isinstance(item, items.Curse)]
            room = world.tile_at(self.x, self.y)
            enemy = room.enemy
            hp_xp = room.enemy.hp
            if curses:
                sorted_curses = sorted(curses, key=lambda item: item.damage, reverse=True)
                if room.enemy is not None and room.enemy.alive is True:
                    print(f"Ok, what curse do you want to cast? You have {self.mana} Mana.")
                    for i, item in enumerate(sorted_curses, 1):
                        print("{}. {} DMG - {} - {} Mana"
                            .format(i, item.damage, item.name, item.mana_cost))
                    user_input = input(">>>> ").lower()
                    if user_input == 'q':
                        print("Don't waste time!\n")
                        break
                    try:
                        n = int(i)
                        choice = int(user_input)
                        try:
                            if choice <= n and choice != 0 and i > 0:
                                chosen_curse = sorted_curses[choice - 1]
                            else:
                                print("Number out of range.\n")
                                return
                        except IndexError:
                            print("Number out of range.\n")
                            return
                    except ValueError:
                        print("ValueError")
                        return

                    if chosen_curse.mana_cost <= self.mana:
                        dice = random.randint(1, 20)
                        if dice in [18, 19, 20]:
                            enemy.hp -= (chosen_curse.damage*2)
                            self.mana -= chosen_curse.mana_cost
                            print("Critical hit!")
                            print(f"You cast {chosen_curse.name} on this {enemy.name}, it does {chosen_curse.damage} DMG! You now have {self.mana} Mana remaining.")
                        else:
                            enemy.hp -= chosen_curse.damage
                            self.mana -= chosen_curse.mana_cost
                            print(f"You cast {chosen_curse.name} on this {enemy.name}, it does {chosen_curse.damage} DMG! You now have {self.mana} Mana remaining.")
                    else:
                        print("You try to cast the curse but you don't have enough Mana! You fail!")
                        return

                    if enemy.hp <= 0:
                        xp_earned = (hp_xp // 2)
                        self.xp += xp_earned
                        print("YEAH! Your curse killed that fucking bastard!")
                        loot = random.randint(10, 200)
                        self.level_up()
                        self.gold = self.gold + loot
                        print(f"The asshole lost his booty. Now {loot} Pine Cones are yours!")
                        room.enemy.alive = False
                        return
                    elif enemy.hp >= 0:
                        print("{} has {} HP remaining.".format(enemy.name, enemy.hp))
                        return
                else:
                    return
            else:
                print("You don't have any curse with you.")
                return


# CALL *** DROP ALL / PICK UP ALL ***
    def drop_all_get_all(self, receiver, giver):
        room = world.tile_at(self.x, self.y)
        for i, item in enumerate(giver.inventory, 0):   # assolutamente inutile, ma è così perché non funziona dropparli uno per uno..
            receiver.inventory.extend(giver.inventory)
            giver.inventory = []
            if receiver is self:
                print(f"{item.name}: taken.")
            if receiver is room:
                print(f"{item.name}: dropped.")

# CALL *** DROP/PICK UP/GIVE LIST***
    def dpg(self, receiver, giver):
        room = world.tile_at(self.x, self.y)
        sorted_inventory = sorted(giver.inventory, key=lambda item: item.name.lower())
        for i, item in enumerate(sorted_inventory, 1):
            print(f" | {i}. {item}")
        while True:
            if giver is self and receiver is room:
                print("What do you want to drop? Choose an item or type 'Q' to quit.")
            elif giver is room and receiver is self:
                print("What do you want to pick up? Choose an item or type 'Q' to quit.")
            else:
                print(f"What do you want to give to {room.talker}? Choose an item or type 'Q' to quit.")
            user_input = input(">>>> ")

            if user_input in ['q', ' ', 'exit', 'no']:
                print("Ok.")
                break
            else:
                try:
                    n = int(i)
                    choice = int(user_input)
                    if choice <= n and choice != 0 and i > 0:
                        chosen_item = sorted_inventory[choice - 1]
                        self.item_donation(giver, receiver, chosen_item)
                        if giver is self and receiver is room:
                            print(f"{chosen_item.name}: dropped")
                            return
                        elif giver is room and receiver is self:
                            print(f"{chosen_item.name}: taken")
                            return
                        elif giver is self and receiver is room.talker:     #TODO if room.talker.accept_object is True, else << I don't want it. >>
                            print(f"{chosen_item.name}: given.")
                            print(f"{room.talker} says to you: << Thank you. >>")
                            return
                        break
                    else:
                        print("Number out of range, try again or type 'Q' to quit")
                        return
                except ValueError:
                    print("Invalid choice, try again or type 'Q' to quit.")
                    continue

    def item_donation(self, giver, receiver, item):
        giver.inventory.remove(item)
        receiver.inventory.append(item)
#        print("You dropped your {}.".format(item.name))

# CALL *** EXAMINE ITEM *** ok proviamo a confrontare i NOMI degli oggetti invece che la classe
    def examine_item(self):
        room = world.tile_at(self.x, self.y)
        chosen_item = []
        print("What do you want to examine?")
        key = input(">>>> ").lower()
        if key in entities_index.stuff:
            thing_to_examine = entities_index.stuff[key]
            chosen_item.append(thing_to_examine)
            stuff_to_examine = {item.name for item in chosen_item}
            stuff_you_own = {item.name for item in self.inventory}
            stuff_in_room = {item.name for item in room.inventory}
            environmental_in_room = {item.name for item in room.env_obj}
            if (set(stuff_to_examine) & set(stuff_you_own) or
                set(stuff_to_examine) & set(stuff_in_room) or
                set(stuff_to_examine) & set(environmental_in_room)):
                print("{}".format(thing_to_examine.description))
                if thing_to_examine.name in "Thermo bottle":
                    if self.bottle_full:
                        print("It's full of fresh water, it heals you for {} HP."
                              .format(thing_to_examine.heal))
                    else:
                        print("It's empty.")
                elif thing_to_examine.damage:
                    print("It deals {} DMG.".format(thing_to_examine.damage))
                elif thing_to_examine.heal:
                    print("It heals you for {} HP.".format(thing_to_examine.heal))
                elif thing_to_examine.defence:
                    print("It protects you with {} DEF.".format(thing_to_examine.defence))
                else:
                    pass
            else:
                print("You can't see any {} here.".format(key))
        elif key == 'all':
            pass            #TODO
        else:
            print("{} is something I don't recognize".format(key))

# CALL *** HEAL ***
    def heal(self):
        consumables = [item for item in self.inventory
                       if isinstance(item, items.Consumable)]
        bottle_list = [item for item in self.inventory
                       if isinstance(item, items.Bottle)]

        if not consumables and not bottle_list:
            print("You've got nothing to heal yourself!")
            return
        elif consumables:
            sorted_consumables = sorted(consumables, key=lambda item: item.heal)
            print(f"Your health is {self.hp}/{self.max_hp}. Choose what you want to cure yourself with or type (Q) to exit:")
            for i, item in enumerate(sorted_consumables, 1):
                print(f"{i}. {item}")

        if bottle_list and self.bottle_full:
            print("Your bottle is full. If you want to drink the water it contains, type (Drink).")
        elif bottle_list:
            print("You have your bottle, but is empty.")

        valid = False
        while not valid:
            choice = input(">>>> ").lower()
            if choice == 'q':
                print("You close your backpack.")
                break
            elif choice == 'drink' and not bottle_list:
                print("You don't have any bottle with you.")
                break
            elif choice == 'drink' and self.bottle_full:
                print(f"You drink the water from the bottle. The water restores your HP by {items.Bottle().heal}.")
                if self.max_hp >= self.hp + items.Bottle().heal:
                    self.hp += items.Bottle().heal
                else:
                    self.hp = self.max_hp
                self.bottle_full = False
                print("Your bottle is now empty.")
                break
            elif choice == 'drink':
                print("Your bottle is empty.")
                break
            try:
                to_eat = sorted_consumables[int(choice) - 1]
                if self.max_hp >= self.hp + to_eat.heal:
                    self.hp += to_eat.heal
                else:
                    self.hp = self.max_hp
                self.inventory.remove(to_eat)
                print(f"You have {self.hp} HP remaining.")
                valid = True
            except (ValueError, IndexError):
                print("Invalid choice, try again.")
                continue


# CALL *** LEVEL UP ***
    def level_up(self):
        if self.xp >= self.xp_modifier:
            self.xp_modifier += 100
            self.lvl += 1
            self.max_hp += 100
            self.hp = self.max_hp
            self.max_mana += 100
            self.mana = self.max_mana
            print(f"You leveled up! You are now at {self.lvl} LVL.")

# CALL *** MAP ***   
    # TODO sarebbe ottimo poter vedere solo le stanze in cui sei stato. ho implementato un bool dentro ogni stanza ma non ho ancora capito come usarlo
    def print_map(self):
        room = world.tile_at(self.x, self.y)
        loc_x = str(self.x)
        loc_y = str(self.y)
        print(f'> You are here: ({loc_x},{loc_y})')
        dsl_lines = world.world_dsl.splitlines()
        dsl_lines = [x for x in dsl_lines if x]

        Black = "|   bs  |"
        Chest = "|   ?   |"
        Enem1 = "|   .1  |"
        Enem2 = "|   .2  |"
        Enem3 = "|   .3  |"
        Enem4 = "|   .4  |"
        Enem5 = "|   .5  |"
        Ferns = "|   f   |"
        Intrd = "|   in  |"
        Littl = "|  (o)  |"
        OakWi = "|   k   |"
        PathT = "|   .   |"
        PathV = "|   .V  |"
        RinaC = "|   rc  |"
        River = "|   r   |"
        Squar = "|   sq  |"
        Start = "|  STR  |"
        Styli = "|  sy   |"
        Templ = "|  Tm   |"
        Taver = "|   t   |"
        TavRo = "|   tr  |"
        Victo = "|  WIN  |"
        VillN = "|   vn  |"
        VillS = "|   vs  |"
        Empty = "         "

        tile_type_dict = {"BS": Black,
                          "!!": Chest,
                          ".1": Enem1,
                          ".2": Enem2,
                          ".3": Enem3,
                          ".4": Enem4,
                          ".5": Enem5,
                          "FT": Ferns,
                          "IN": Intrd,
                          "Lo": Littl,
                          "OK": OakWi,
                          "..": PathT,
                          ".V": PathV,
                          "RC": RinaC,
                          "RV": River,
                          "SQ": Squar,
                          "SS": Start,
                          "SY": Styli,
                          "TM": Templ,
                          "TT": Taver,
                          "TR": TavRo,
                          "WW": Victo,
                          "Vn": VillN,
                          "Vs": VillS,
                          "  ": Empty}
        # spazi tra le stanze personalizzati:
        nonempty_ceil = " _______ "
        nonempty_wall = "|       |"
        nonempty_floo = "|_______|"

        empty_floo = "         "
        empty_ceil = "         "
        empty_wall = "         "
        for y, dsl_row in enumerate(dsl_lines):
            ceiling = []
            floor = []
            wall = []
            row = []
            dsl_cells = dsl_row.split("|")
            dsl_cells = [c for c in dsl_cells if c]
            for dsl_cell in dsl_cells:
                map_tile_type = tile_type_dict[dsl_cell]
                row.append(map_tile_type)
                if dsl_cell in ["  ", ""]:
                    ceiling.append(empty_ceil)
                    floor.append(empty_floo)
                    wall.append(empty_wall)
                else:
                    ceiling.append(nonempty_ceil)
                    floor.append(nonempty_floo)
                    wall.append(nonempty_wall)
            print("".join(ceiling))
            print("".join(wall))
            print("".join(row))
            print("".join(floor))



# CALL *** OPEN ***
    def open_obj(self):
        room = world.tile_at(self.x, self.y)
        if room.env_obj.can_be_open:
            if room.env_obj.inventory:
                print(f"You open the {room.env_obj}.")
                for i, item in enumerate(room.env_obj.inventory, 1):
                    print(f"{i}. {item}")
                user_input = input("Choose what you want to get or type (Q) to exit.\n>>>> ").lower()
                while True:
                    if user_input == 'q':
                        print(f"You close the {room.env_obj}.")
                        return
                    else:
                        try:
                            n = int(i)
                            choice = int(user_input)
                            if choice <= n and choice != 0 and i > 0:
                                chosen_item = room.env_obj.inventory[choice - 1]
                                room.env_obj.inventory.remove(chosen_item)
                                self.inventory.append(chosen_item)
                                print(f"{chosen_item.name}: taken")
                                break
                            else:
                                print("Number out of range, try again or type 'Q' to quit")
                                continue
                        except ValueError:
                            print("Invalid choice, try again or type 'Q' to quit.")
                            continue
            else:
                print("There is nothing interesting in here")
                return
        else:
            room.open_quest(self)

# CALL *** RECHARGE MANA ***
    def recharge_mana(self):

        # Creates a separate list of items that reload mana
        mrs = [item for item in self.inventory
                       if isinstance(item, items.ManaRechargers)]
        if not mrs:
            print("You've got nothing to recharge your Mana!")
            return

        # If the list is not empty, it puts them in order of recharge power
        elif mrs:
            sorted_mrs = sorted(mrs, key=lambda item: item.mr, reverse=True)
            print(f"Your mana is {self.mana}/{self.max_mana}. Choose or type (Q) to exit:")
            for i, item in enumerate(sorted_mrs, 1):
                print(f"{i}. {item}")

        # Allows to choose which one to consume
        valid = False
        while not valid:
            choice = input(">>>> ".lower())
            if choice == 'q':
                print("You close your backpack.")
                break
            try:
                to_consume = sorted_mrs[int(choice) - 1]
                if self.max_mana >= self.mana + to_consume.mr:
                    self.mana += to_consume.mr
                else:
                    self.mana = self.max_mana
                self.inventory.remove(to_consume)
                print(f"You now have {self.mana} Mana.")
                valid = True
            except (ValueError, IndexError):
                print("Invalid choice, try again.")
                continue

# CALL *** ROOM VISITED ***
    def room_visited(self):
        room = world.tile_at(self.x, self.y)
        room.room_seen(self)

# CALL *** RUN ***
    def run(self):
        # Rolls a d20 to decide if you can escape the fight
        room = world.tile_at(self.x, self.y)
        d20 = random.randint(1,20)
        if d20 == 20:
            room.enemy.alive = False
            print("No need to do this. You enemy is dead.")
        if d20 > 15 and d20 < 20:
            print("You flee.")
            self.x = self.previous_x
            self.y = self.previous_y
        else:
            print("You can't escape!")
            return

# CALL *** SAVE & RESTORE ***
    # TODO aggiungi room.seen che probabilmente servirà per la mappa
    # TODO verifica il funzionamento corretto della stanza della taverna (se rimane chiusa o aperta come dovrebbe)

    # Function that creates a list of rooms with no empty spaces from the world map
    def room_list_creator(self):
        rooms_list_with_empty_spaces = []
        for tile in world.world_map_caller():
            rooms_list_with_empty_spaces.extend(tile)

        for room in rooms_list_with_empty_spaces:
            if isinstance(room, world.MapTile):
                self.rooms_list.append(room)

    def save(self):
        # Checks if the save files already exist and if so, delete them.
        if os.path.isfile('./saved_data.pkl'):
            os.remove("saved_data.pkl")
            print("Deleting old saved data...")

        player_data = {
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'inventory': self.inventory,
            'level': self.lvl,
            'max_hp': self.max_hp,
            'hp': self.hp,
            'max_mana': self.max_mana,
            'mana': self.mana,
            'xp': self.xp,
            'xp_modifier': self.xp_modifier,
            'base_defence': self.base_defence,
            'current_weapon': self.current_weapon,
            'carryweight': self.carryweight,
            'gold': self.gold,
            'victory': self.victory,
            'previous_x': self.previous_x,
            'previous_y': self.previous_y,
            'turn': self.turn,
            'verbose': self.verbose,
            'bottle_full': self.bottle_full,

            'tavern_room_paid': self.tavern_room_paid,

            'ferns_talked': self.ferns_talked,
            'specimen_received' : self.specimen_received,
            'ferns_price_received' : self.ferns_price_received,

            'specimen_planted': self.specimen_planted,
            'oracle_response': self.oracle_response,

            'rina_gift_received': self.rina_gift_received
        }

        # Recreate a list of rooms with no gaps, updating it at the current state 
        self.rooms_list == []
        self.room_list_creator()

        # Creates lists of enemies, inventories, npcs and env objs on the map
        rooms_inventories = []
        world_enemies = []
        world_npcs = []
        world_env_objs = []
        for room in self.rooms_list:
            rooms_inventories.append(room.inventory)
            if room.enemy:
                world_enemies.append(room.enemy)
            if room.talker:
                world_npcs.append(room.talker)
            if room.env_obj:
                world_env_objs.append(room.env_obj)

        # Creates a list of all rooms with a chest
        chest_rooms = [room for room in self.rooms_list
                   if isinstance(room, world.ChestTile)]

        # Saves all lists in the same file
        with open('saved_data.pkl', 'wb') as write:
            pickle.dump(player_data, write)
            pickle.dump(rooms_inventories, write)
            pickle.dump(world_enemies, write)
            pickle.dump(world_npcs, write)
            pickle.dump(world_env_objs, write)
            pickle.dump(chest_rooms, write)

    def restore(self):
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
        self.name = player_data['name']
        self.x = player_data['x']
        self.y = player_data['y']
        self.inventory = player_data['inventory']
        self.lvl = player_data['level']
        self.max_hp = player_data['max_hp']
        self.hp = player_data['hp']
        self.max_mana = player_data['max_mana']
        self.mana = player_data['mana']
        self.xp = player_data['xp']
        self.xp_modifier = player_data['xp_modifier']
        self.current_weapon = player_data['current_weapon']
        self.carryweight = player_data['carryweight']
        self.gold = player_data['gold']
        self.victory = player_data['victory']
        self.previous_x = player_data['previous_x']
        self.previous_y = player_data['previous_y']
        self.turn = player_data['turn']
        self.verbose = player_data['verbose']
        self.bottle_full = player_data['bottle_full']

        self.tavern_room_paid = player_data['tavern_room_paid']

        self.ferns_talked = player_data['ferns_talked']
        self.specimen_received = player_data['specimen_received']
        self.ferns_price_received = player_data['ferns_price_received']

        self.specimen_planted = player_data['specimen_planted']
        self.oracle_response = player_data['oracle_response']

        self.rina_gift_received = player_data['rina_gift_received']

        # Check if a list of rooms with no gaps has already been created to avoid duplicates
        if self.rooms_list == []:
            self.room_list_creator()
        
        rooms_with_enemies = []
        rooms_with_npcs = []
        rooms_with_env_objs = []
        for i, room in enumerate(self.rooms_list, 0):
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
        cur_chest_rooms = [room for room in self.rooms_list
                   if isinstance(room, world.ChestTile)]
        # Changes the "closed" variable of the current room and makes it the same as that of the saved room
        for i, room in enumerate(cur_chest_rooms, 0):
            room.closed = chest_rooms[i].closed

        print("Your progress has been restored.")

# CALL *** TALK ***
    def check_dialogue(self):
        room = world.tile_at(self.x, self.y)
        room.dialogue(self)

# CALL *** TRADE ***
    def trade(self, buyer, seller):
    # This function is called both if the player buys and sells.
    # The roles are decided by the dialogue with the trader,
    # where this function is called by assigning the right parameters.

        # Creates separate lists for different types of items
        right_order_list = []
        room = world.tile_at(self.x, self.y)
        index = 1
        weapons = [item for item in seller.inventory
                       if isinstance(item, items.Weapon)]
        curses = [item for item in seller.inventory
                       if isinstance(item, items.Curse)]
        consumables = [item for item in seller.inventory
                       if isinstance(item, items.Consumable)]
        mrs = [item for item in seller.inventory
                       if isinstance(item, items.ManaRechargers)]
        armors = [item for item in seller.inventory
                       if isinstance(item, items.Armor)]

        # Sorts items alphabetically but adds them sorted and numbered to the
        # right_order_list only if the player is trading with the trader who 
        # exclusively trades that particular kind of item (Merchant trades 
        # them all). Two different prices are displayed because the items sold 
        # by the player are worth less money.
        if weapons and room.talker.name in ['Blacksmith', 'Merchant']:
            sorted_weapons = sorted(weapons, key=lambda item: item.damage, reverse=True)
            for i, item in enumerate(sorted_weapons, index):
                if buyer == room.talker:
                    print(f"{i}. {item.damage} DMG - {item.name} - {item.if_sold} §")
                else:
                    print(f"{i}. {item.damage} DMG - {item.name} - {item.value} §")
                index += 1
                right_order_list.append(item)
        if curses and room.talker.name in ['Little(o)', 'Merchant']:
            sorted_curses = sorted(curses, key=lambda item: item.damage, reverse=True)
            for i, item in enumerate(sorted_curses, index):
                if buyer == room.talker:
                    print(f"{i}. {item.damage} DMG - {item.name} - {item.if_sold} §")
                else:
                    print(f"{i}. {item.damage} DMG - {item.name} - {item.value} §")
                index += 1
                right_order_list.append(item)
        if consumables and room.talker.name in ['Innkeeper', 'Merchant']:
            sorted_consumables = sorted(consumables, key=lambda item: item.heal, reverse=True)
            for i, item in enumerate(sorted_consumables, index):
                if buyer == room.talker:
                    print(f"{i}. +{item.heal} HP - {item.name} - {item.if_sold} §")
                else:
                    print(f"{i}. +{item.heal} HP - {item.name} - {item.value} §")
                index += 1
                right_order_list.append(item)
        if mrs and room.talker.name in ['Monk', 'Merchant']:
            sorted_mrs = sorted(mrs, key=lambda item: item.mr, reverse=True)
            for i, item in enumerate(sorted_mrs, index):
                print(f"{i}. +{item.mr} Mana - {item.name} - {item.value} §")
                index += 1
                right_order_list.append(item)
        if armors and room.talker.name in ['Blacksmith', 'Merchant']:
            sorted_armors = sorted(armors, key=lambda item: item.defence, reverse=True)
            for i, item in enumerate(sorted_armors, index):
                if buyer == room.talker:
                    print(f"{i}. +{item.defence} DEF - {item.name} - {item.if_sold} §")
                else:
                    print(f"{i}. +{item.defence} DEF - {item.name} - {item.value} §")
                index += 1
                right_order_list.append(item)

        # If there are items in the list, it allows you to decide 
        # which to sell or buy by calling the "swap" function
        if not right_order_list:
            print("\n> The merchant examines the things you have to offer...\n")
            print("<< You have nothing that interests me. >>")
            return
        while True:
            print(f"You have {self.gold} §: choose an item or press 'Q' to quit.")
            user_input = input(">>>> ")
            if user_input in ['Q', 'q']:
                print("<< As you wish, precious customer. >>")
                break
            else:
                try:
                    n = int(i)
                    choice = int(user_input)
                    try:
                        if choice <= n and choice != 0 and i > 0:
                            chosen_item = right_order_list[choice - 1]
                            self.swap(seller, buyer, chosen_item)
                            if seller is room.talker and chosen_item.value <= buyer.gold:
                                print(f"<< Here's your brand new {chosen_item.name}, customer. >>")
                                return
                            elif seller is room.talker:
                                pass
                            elif seller is self:
                                print(f"<< Thanks for your {chosen_item.name}. >>")
                                return
                            break           # è giusto perché deve uscire dal loop per poter riscrivere l'inventario dato che l'indicizzazione è cambiata essendoci un oggetto in meno
                        else:
                            print("Number out of range, try again or type 'Q' to quit.")
                            continue
                    except IndexError:
                        print("<< Out of stock, please come back later. >>")
                        break
                except ValueError:
                    print("Invalid choice, try again or type 'Q' to quit.")
                    continue

    def swap(self, seller, buyer, item):
        # Exchanges items sold and bought between you and the trader and modify 
        # the money of both. The trader's money does not decrease if he buys 
        # to prevent them from running out of gold to be able to buy more from you
        room = world.tile_at(self.x, self.y)
        if item.value > buyer.gold:
            print("<< You don't have enough cash. >>")
            return
        if buyer == room.talker:
            seller.gold += item.if_sold
        else:
            seller.gold += item.value
            buyer.gold -= item.value
        #  buyer.gold -= item.if_sold
        seller.inventory.remove(item)
        buyer.inventory.append(item)