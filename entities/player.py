import contextlib
import random

from .entities_templates import Weapon, Curse, Armor, Healer
from .factories.weapons_factory import WeaponsFactory as weapon
from .factories.curses_factory import CursesFactory as curse
from .factories.armors_factory import ArmorsFactory as armor
from .factories.healers_factory import HealersFactory as healer

import world.parser as parser
import world.tiles as world


# MODULO DEL GIOCATORE
class Player:
    def __init__(self):
        self.name = 'Your Name Here'
        self.x = parser.start_tile_location[0]       # modifica questi valori per modificare la locazione di partenza. di base è su (0, 1)
        self.y = parser.start_tile_location[1]       # ma in realtà la locazione di partenza è determinata da dove metti la StartTile
        self.inventory = [weapon().manuport, armor().tesla_armor]
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
        room = parser.tile_at(self.x, self.y)
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
            response += (
                f"\nCritical hit! "
                f"You deal {best_weapon.damage * damage_multiplier} DMG!"
            )
        elif precision in [17, 18, 19]:
            damage_multiplier = 1.5
            response += (
                f"\nGood hit! "
                f"You deal {best_weapon.damage * damage_multiplier} DMG!"
            )
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
            response += (
                f"\nYEAH! You killed that fucking bastard! "
                f"You earned {xp_earned} XP!"
            )

            loot = random.randint(10,200)
            self.level_up()
            self.gold += loot
            response += (
                f"\nThe asshole lost his booty. "
                f"Now {loot} Pine Cones are yours!"
            )
            enemy.alive = False
        else:
            response += f"\n{enemy.name} has {enemy.hp} HP remaining."

        return response


    # *** BEST WEAPON ***
    def best_weapon(self):
        max_damage = 0
        best_weapon = None
        if weapons := [
            item for item in self.inventory if isinstance(item, Weapon)
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
    def sort_items_by_category(self, inventory, category):
        return sorted([item for item in inventory if isinstance(item, category)], key=lambda item: item.name.lower())


    def choose_response(func):
        def wrapper(self, *args):
            response = ""
            if args[0] == self.inventory:
                response += f"\nYour wealth: {self.gold} §"
                response += "\nChoose a number to read an item's description or press Q to quit."
    
                
            elif args[1] == Armor and args[2] == self.inventory:
                response = f"Your defence is now {self.base_defence}."
            else:
                pass
            return func(self, *args) + response
        return wrapper


    @choose_response
    def show_inventory(self, *args):
        inventory = args[0]
        response = ""
        right_order_list = []
        index = 1
        
        for category in [Weapon, Curse, Healer, Armor]:
            items_in_category = self.sort_items_by_category(inventory, category)

            if items_in_category:
                response += f"\n>> {category.__name__.upper()}:\n"

                for _, item in enumerate(items_in_category, index):
                    response += f"{index}. {item.name}"
                    index += 1
                    right_order_list.append(item)
        inventory = right_order_list
        return response


    @choose_response
    def choose_item(self, *args):
        action = args[0]
        inventory = args[2]

        if action.lower() in ('q', 'exit', 'no'):
            return "Ok."
        try:
            choice = int(action)-1
            to_read = inventory[choice]
            return f"{to_read.name}: {to_read.description}"
        except (ValueError, IndexError):
            return "Invalid choice, try again."


    # *** DIAGNOSE ***
    def diagnose(self):
        return (
            f"You have {self.hp}/{self.max_hp} HP and {self.mana}/{self.max_mana} Mana remaining. This is turn number {self.turn}."
        )


    # *** MAP ***   
    def show_map(self):
        Black = "| bs |"
        Chest = "| ?  |"
        Enem1 = "| .1 |"
        Enem2 = "| .2 |"
        Enem3 = "| .3 |"
        Enem4 = "| .4 |"
        Enem5 = "| .5 |"
        Ferns = "| f  |"
        Intrd = "| in |"
        Littl = "| (o)|"
        OakWi = "| k  |"
        PathT = "| .  |"
        PathV = "| .V |"
        RinaC = "| rc |"
        River = "| r  |"
        Squar = "| sq |"
        Start = "| STR|"
        Styli = "| sy |"
        Templ = "| Tm |"
        Taver = "| t  |"
        TavRo = "| tr |"
        Victo = "| WIN|"
        VillN = "| vn |"
        VillS = "| vs |"
        Empty = "      "

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
        
        loc_x = str(self.x)
        loc_y = str(self.y)
        dsl_lines = parser.world_dsl.splitlines()
        dsl_lines = [x for x in dsl_lines if x]
        for _, dsl_row in enumerate(dsl_lines):
            row = []
            dsl_cells = dsl_row.split("|")
            dsl_cells = [c for c in dsl_cells if c]
            for dsl_cell in dsl_cells:
                map_tile_type = tile_type_dict[dsl_cell]
                row.append(map_tile_type)
            print("".join(row))
        print(f'> You are here: ({loc_x},{loc_y})')


# FIXME: All these methods need to be fixed
# Call TAVERN ROOM CLOSED**
    def tavern_room_closed(self):
        print("The room door is closed.")
        return

# CALL *** ALIVE ***
    def is_alive(self):
        return self.hp > 0


    # TODO: *** CAST CURSE ***
    def cast_curse(self):
        pass


# CALL *** DROP ALL / PICK UP ALL ***
    def drop_all_get_all(self, receiver, giver):
        room = parser.tile_at(self.x, self.y)
        for i, item in enumerate(giver.inventory, 0):   # assolutamente inutile, ma è così perché non funziona dropparli uno per uno..
            receiver.inventory.extend(giver.inventory)
            giver.inventory = []
            if receiver is self:
                print(f"{item.name}: taken.")
            if receiver is room:
                print(f"{item.name}: dropped.")


    # CALL *** DROP/PICK UP/GIVE LIST***
    def item_handler(self, action, receiver, giver):
        room = parser.tile_at(self.x, self.y)
        sorted_inventory = sorted(giver.inventory, key=lambda item: item.name.lower())

        if giver is self and receiver is room:
            prompt = "What do you want to drop?"
            success_msg = "Dropped."
        elif giver is room and receiver is self:
            prompt = "What do you want to pick up?"
            success_msg = "Taken."
        else:
            prompt = f"What do you want to give to {room.talker}?"
            success_msg = "Given."

        chosen_item = self.choose_item(sorted_inventory, prompt)
        if chosen_item is None:
            return "Ok."

        self.item_donation(giver, receiver, chosen_item)
        if action == "give" and giver is self and receiver is room.talker:
            if room.talker.accept_object:
                return (
                    f"{room.talker} says to you: << Thank you. >>"
                    f"{chosen_item.name}: {success_msg}"
                )
            else:
                return f"{room.talker} says to you: << I don't want it. >>"

    def choose_item_handler(self, sorted_inventory, prompt):
        response = ""
        for i, item in enumerate(sorted_inventory, 1):
            response += f" | {i}. {item}"
            
        while True:
            user_input = input(f"{prompt} Choose an item or type 'Q' to quit.\n>>>> ")
            if user_input in ['q', ' ', 'exit', 'no']:
                return None
            try:
                choice = int(user_input)
                if choice not in range(1, len(sorted_inventory) + 1):
                    raise ValueError
                return sorted_inventory[choice - 1]
            except (ValueError, IndexError):
                print("Invalid choice, try again.")

    def item_donation(self, giver, receiver, item):
        giver.inventory.remove(item)
        receiver.inventory.append(item)
    

    # TODO: *** HEAL ***
    def heal(self):
        pass


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


    # TODO: *** OPEN ***
    def open_obj(self):
        pass
    

    # TODO: *** RECHARGE MANA ***
    def recharge_mana(self):
        pass


# CALL *** ROOM VISITED ***
    def room_visited(self):
        room = parser.tile_at(self.x, self.y)
        room.room_seen(self)

# CALL *** RUN ***
    def run(self):
        # Rolls a d20 to decide if you can escape the fight
        room = parser.tile_at(self.x, self.y)
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


    # Function that creates a list of rooms with no empty spaces from the world map
    def room_list_creator(self):
        rooms_list_with_empty_spaces = []
        for tile in parser.world_map_caller():
            rooms_list_with_empty_spaces.extend(tile)

        for room in rooms_list_with_empty_spaces:
            if isinstance(room, world.MapTile):
                self.rooms_list.append(room)


# CALL *** TALK ***
    def check_dialogue(self):
        room = parser.tile_at(self.x, self.y)
        room.dialogue(self)


    # TODO: *** TRADE ***
    def trade(self, buyer, seller):
        pass

