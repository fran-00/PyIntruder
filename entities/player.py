import contextlib
import random

from .entities_templates import Weapon, Curse, Armor, Healer
from .factories.weapons_factory import WeaponsFactory as Wf
from .factories.curses_factory import CursesFactory as Cf
from .factories.armors_factory import ArmorsFactory as Af
from .factories.healers_factory import HealersFactory as Hf

import world.parser as parser
import world.tiles as world


class Player:
    def __init__(self):
        self.name = 'Your Name Here'
        self.x = parser.start_tile_location[0]
        self.y = parser.start_tile_location[1]

        self.items = [Wf().wire,
                      Wf().manuport,
                      Wf().deliverance,
                      Af().tesla_armor]
        self.inventory = self.sort_inventory(self.items)
        self.current_weapon = self.best_weapon()
        self.gold = 10000000

        self.turn = 0
        self.is_selling = False
        self.lvl = 1
        self.max_hp = 100
        self.hp = 100
        self.max_mana = 100
        self.mana = 100
        self.xp = 0
        self.xp_modifier = 100
        self.base_defence = 0

    # -------------------------------------------------------------------------|
    # MOVEMENT ----------------------------------------------------------------|
    # -------------------------------------------------------------------------|

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

    # -------------------------------------------------------------------------|
    # COMBAT ------------------------------------------------------------------|
    # -------------------------------------------------------------------------|

    def attack(self):
        """Attacks the enemy in the current room with the best available weapon and return a message describing the outcome of the attack.

        Returns:
            str: A message describing the outcome of the attack, including any damage dealt or loot obtained.
        """
        best_weapon = self.best_weapon()
        room = parser.tile_at(self.x, self.y)
        enemy = room.enemy
        response = ""

        if best_weapon is None:
            return "You don't have any weapon with you."

        if enemy is None or not enemy.alive:
            return

        response += f"You try to hit {enemy.name} with {best_weapon.name}!"
        precision = random.randint(1, 20)

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

            loot = random.randint(10, 200)
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

    def best_weapon(self):
        """Finds the best weapon in the player's inventory and return it.

        Returns:
            Weapon or None: The best weapon in the player's inventory, or None if the player has no weapons.
        """
        max_damage = 0
        best_weapon = None
        if weapons := [
            item for item in self.inventory if isinstance(item, Weapon)
        ]:
            for _, item in enumerate(weapons, 1):
                with contextlib.suppress(AttributeError):
                    if item.damage > max_damage:
                        best_weapon = item
                        max_damage = item.damage
            return best_weapon
        else:
            return None

    # -------------------------------------------------------------------------|
    # INVENTORY AND TRADING SYSTEM --------------------------------------------|
    # -------------------------------------------------------------------------|

    def sort_inventory(self, items):
        for category in [Weapon, Curse, Healer, Armor]:
            return sorted([item for item in items if isinstance(item, category)], key=lambda item: item.name.lower())

    def pre_trading(self, *args):
        return "Buy, Sell or Quit?"

    def trading_mode(self, *args):
        action = args[-1]
        room = parser.tile_at(self.x, self.y)
        if action == "b":
            return self.show_inventory(room.talker.inventory, True)
        elif action == "s":
            self.is_selling = True
            return self.show_inventory(self.inventory, True)
        elif action == "q":
            return None
        else:
            return "Invalid choice, try again."

    def show_instructions(func):
        def wrapper(self, *args):
            room = parser.tile_at(self.x, self.y)
            response = ""
            if args[0] == self.inventory:
                response += f"\nYour wealth: {self.gold} §"
                response += "\nChoose a number to read an item's description or press Q to quit."
            elif room.talker and args[0] == room.talker.inventory:
                response += "\nChoose a number to buy an item or press Q to quit."
            else:
                pass
            return func(self, *args) + response
        return wrapper

    @show_instructions
    def show_inventory(self, *args):
        """Displays items in an inventory, sorted by category.
        Data shown depends on the action to be taken in the inventory, 
        such as seeing the description of an item, selling it or buying it

        Args:
            inventory (list): A list of Item objects representing inventory.
            trade (bool): A boolean flag indicating whether the inventory is 
            being viewed for trading purposes.

        Returns:
            str: A string representation of the inventory, formatted as a list 
            of items sorted by category and name.
        """
        inventory = args[0]
        trade = args[1]
        response = ""
        index = 1

        for category in [Weapon, Curse, Healer, Armor]:
            items_in_category = self.sort_items_by_category(
                inventory, category)

            if items_in_category:
                response += f">> {category.__name__.upper()}:\n"

            if not trade:
                for _, item in enumerate(items_in_category, index):
                    response += f"{index}. {item.name}\n"
                    index += 1
            else:
                for _, item in enumerate(items_in_category, index):
                    response += f"{index}. DMG: {item.damage} - {item.name} - {item.value}$\n"
                    index += 1
        return response

    def sort_items_by_category(self, inventory, category):
        return sorted([item for item in inventory if isinstance(item, category)], key=lambda item: item.name.lower())

    def choose_item(self, *args):
        """Selects an item from the inventory based on the user's input.

        Args:
            *args (tuple): A tuple of arguments containing the user's input `action`,
                `inventory` list, and `trade` boolean.

        Returns:
            str: A string representing the appropriate response based on the user's input.
        """
        if not self.is_selling:
            inventory = args[0]
        else:
            inventory = self.inventory
        trade = args[1]    
        action = args[-1]

        if action.lower() in ('q', 'exit', 'no'):
            return "Ok. Action cancelled."
        try:
            item_index = int(action)
            choice = inventory[item_index - 1]
            return self.show_appropriate_answer(choice, trade)
        except Exception as e:
            return f"{e}"

    def show_appropriate_answer(self, choice, trade):
        room = parser.tile_at(self.x, self.y)
        if not trade:
            return f"{choice.name}: {choice.description}"
        elif trade and self.is_selling:
            self.trade(self, room.talker, choice)
            self.is_selling = False
            return f"Bye {choice.name}!"
        elif trade and not self.is_selling:
            self.trade(room.talker, self, choice)
            return f"Good! Now {choice.name} is yours!"

    def trade(self, seller, buyer, item):
        if item.value > buyer.gold:
            return "<< You don't have enough cash. >>"
        seller.gold += item.value
        buyer.gold -= item.value
        seller.inventory.remove(item)
        buyer.inventory.append(item)

    # -------------------------------------------------------------------------|
    # INFO --------------------------------------------------------------------|
    # -------------------------------------------------------------------------|

    def diagnose(self):
        return (
            f"You have {self.hp}/{self.max_hp} HP and {self.mana}/{self.max_mana} Mana remaining. This is turn number {self.turn}."
        )

    def show_map(self):
        """Prints a textual representation of the world map, with the current location of the player marked.

        The map is defined in the `world_dsl` funcion of `parser` module, and is parsed into a grid of string
        representations of the different types of map tiles. The `tile_type_dict` dictionary maps each tile type to its
        corresponding string representation. The map is printed row by row, with each tile represented by a string enclosed
        in vertical bars.
        """

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

    def is_alive(self):
        return self.hp > 0

    def cast_curse(self):
        pass

    def drop_all_get_all(self, receiver, giver):
        room = parser.tile_at(self.x, self.y)
        for _, item in enumerate(giver.inventory, 0):
            receiver.inventory.extend(giver.inventory)
            giver.inventory = []
            if receiver is self:
                print(f"{item.name}: taken.")
            if receiver is room:
                print(f"{item.name}: dropped.")

    def item_handler(self, action, receiver, giver):
        room = parser.tile_at(self.x, self.y)
        sorted_inventory = sorted(
            giver.inventory, key=lambda item: item.name.lower())

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
            user_input = input(
                f"{prompt} Choose an item or type 'Q' to quit.\n>>>> ")
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

    def heal(self):
        pass

    def level_up(self):
        if self.xp >= self.xp_modifier:
            self.xp_modifier += 100
            self.lvl += 1
            self.max_hp += 100
            self.hp = self.max_hp
            self.max_mana += 100
            self.mana = self.max_mana
            print(f"You leveled up! You are now at {self.lvl} LVL.")

    def open_obj(self):
        pass

    def recharge_mana(self):
        pass

    def room_visited(self):
        room = parser.tile_at(self.x, self.y)
        room.room_seen(self)

    def run(self):
        room = parser.tile_at(self.x, self.y)
        d20 = random.randint(1, 20)
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

    def room_list_creator(self):
        rooms_list_with_empty_spaces = []
        for tile in parser.world_map_caller():
            rooms_list_with_empty_spaces.extend(tile)

        for room in rooms_list_with_empty_spaces:
            if isinstance(room, world.MapTile):
                self.rooms_list.append(room)

    def check_dialogue(self):
        room = parser.tile_at(self.x, self.y)
        room.dialogue(self)
