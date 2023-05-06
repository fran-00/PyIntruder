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

        self.inventory = [Cf().veridical,
                      Wf().wire,
                      Af().fungine_armor,
                      Hf().ats,
                      Wf().deliverance,
                      Cf().cluster_point,
                      Af().tesla_armor,
                      ]
        self.sort_inventory()
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
        self.previous_x = None
        self.previous_y = None

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

    def get_coordinates(self, dx, dy):
        self.previous_x = self.x
        self.previous_y = self.y
        self.move(dx=dx, dy=dy)

    # -------------------------------------------------------------------------|
    # COMBAT ------------------------------------------------------------------|
    # -------------------------------------------------------------------------|

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
                if item.damage > max_damage:
                    best_weapon = item
                    max_damage = item.damage
            return best_weapon
        else:
            return None

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

        if enemy is None or not enemy.is_alive():
            return

        response += f"You try to hit {enemy.name} with {best_weapon.name}!"
        precision = random.randint(1, 20)
        
        match precision:
            case 20:
                damage_multiplier = 2
                response += (
                    f"\nCritical hit! "
                    f"You deal {best_weapon.damage * damage_multiplier} DMG!"
                )
            case 17 | 18 | 19:
                damage_multiplier = 1.5
                response += (
                    f"\nGood hit! "
                    f"You deal {best_weapon.damage * damage_multiplier} DMG!"
                )
            case 3 | 2 | 1:
                response += "\nMissed!"
                return response
            case _:
                damage_multiplier = 1
                response += f"\nYou deal {best_weapon.damage} DMG!"

        enemy.hp -= best_weapon.damage * damage_multiplier
        return self.check_enemy_hp(enemy, response)

    def check_enemy_hp(self, enemy, response):
        # FIXME: Move xp calculation to a specific method
        # xp_earned = (enemy.hp // 2)
        if enemy.hp <= 0:
            # self.xp += xp_earned
            response += (
                f"\nYEAH! You killed it! "
                # f"\nYou earned {xp_earned} XP!"
            )

            loot = random.randint(10, 200)
            # self.level_up()
            self.gold += loot
            response += (
                f"\nThe asshole lost his booty. "
                f"Now {loot} § are yours!"
            )

        else:
            response += f"\n{enemy.name} has {enemy.hp} HP remaining."
        return response

    def cast_curse(self, enemy, choice):
        if choice.mana_cost > self.mana:
            return f"You don't have enough mana to cast {choice.name}!"
        else:
            enemy.hp -= choice.damage
            self.mana -= choice.mana_cost
            return (f"You cast {choice.name} on {enemy.name}, it does {choice.damage} DMG!\n"
                   f"You now have {self.mana} Mana remaining.")

    def flee_from_fight(self):
        room = parser.tile_at(self.x, self.y)
        d20 = random.randint(1, 20)
        if d20 == 20:
            room.enemy.alive = False
            return "No need to do this. Enemy is dead!"
        if d20 > 15 and d20 < 20:
            self.x = self.previous_x
            self.y = self.previous_y
            # FIXME: it doesn't work! Enemy still attacks because loop is
            # still running and an AttributeError is raised if attacking again
            # when you call tile_at method from parser:
            # parser.tile_at(self.previous_x, self.previous_y)
            return "You flee."
        else:
            return"You can't escape!"

    # -------------------------------------------------------------------------|
    # INVENTORY AND TRADING SYSTEM --------------------------------------------|
    # -------------------------------------------------------------------------|

    def sort_inventory(self):
        self.inventory.sort(key=lambda x: (x.__class__.__name__, x.name))
        return

    def trading_mode(self, *args):
        action = args[-1]
        room = parser.tile_at(self.x, self.y)
        match action:
            case "b":
                return self.check_inventory(room.talker.inventory, "trade")
            case "s":
                self.is_selling = True
                return self.check_inventory(self.inventory, "trade")
            case "q":
                return "Come back when you want to trade!", None
            case _:
                return "Invalid choice, try again.", None

    def show_instructions(func):
        def wrapper(self, *args):
            purpose = args[1]
            match purpose:
                case "my-inventory":
                    response = f"Your wealth: {self.gold} §\nChoose a number to read an item's description or press Q to quit."
                case "trade" if not self.is_selling:
                    response = "Choose a number to buy an item or press Q to quit."
                case "trade" if self.is_selling:
                    response = "Choose a number to sell an item or press Q to quit."
                case "pick-up":
                    response = "What do you want to pick up?\nChoose an item or press Q to quit."
                case "drop":
                    response = "What do you want to drop?\nChoose an item or press Q to quit."
                case "Curse":
                    response = f"Ok, what curse do you want to cast? You have {self.mana} Mana."
                case "Healer":
                    response = f"Your health is {self.hp}/{self.max_hp}. Choose what you want to cure yourself with or type (Q) to exit."
                case _:
                    ""
            return func(self, *args) + response
        return wrapper
    
    def check_inventory(self, *args):
        inventory = args[0]
        purpose = args[1]
        
        if purpose in [Armor.__name__, Curse.__name__, Healer.__name__, Weapon.__name__]:
            category = globals()[purpose]
            items_subset = self.sort_items_by_category(self.inventory, category)
            if items_subset == []:
                return f"You don't have any {purpose} with you", None
            else:
                return self.show_inventory(inventory, purpose)
        else:
            if inventory == []:
                match purpose:
                    case "my-inventory":
                        return f"Your inventory is empty!\n You have {self.gold} §.", None
                    case "trade" if self.is_selling:
                        return "You don't have anything to sell!", None
                    case "trade" if not self.is_selling:
                        return "Out of stock! Come back later!", None
                    case "pick-up":
                        return "There is nothing to pick up.", None
                    case "drop":
                        return "You don't have anything to drop.", None
            else:
                return self.show_inventory(inventory, purpose)

    @show_instructions
    def show_inventory(self, *args):
        inventory = args[0]
        purpose = args[1]
        index = 1
        response = ""
        
        if purpose in [Armor.__name__, Curse.__name__, Healer.__name__, Weapon.__name__]:
            category = globals()[purpose]
            items_subset = self.sort_items_by_category(self.inventory, category)
            if items_subset != []:
                for _, item in enumerate(items_subset, index):
                    response += f"{index}. {item}\n"
                    index += 1
        else:
            for parent in [Armor, Curse, Healer, Weapon]:
                items_subset = self.sort_items_by_category(inventory, parent)

                if items_subset:
                    response += f">> {parent.__name__.upper()}S:\n"

                for _, item in enumerate(items_subset, index):
                    if purpose in ["trade"]:
                        response += f"{index}. - {item} - {item.value}§\n"
                    else:
                        response += f"{index}. {item.name}\n"
                    index += 1
        return response

    def sort_items_by_category(self, inventory, category):
        return sorted([item for item in inventory if isinstance(item, category)], key=lambda item: item.name.lower())

    def choose_item(self, *args):
        """Selects an item from the inventory based on the user's input.

        Args:
            *args (tuple): A tuple of arguments containing the user's input `action`,
                `inventory` list, and `purpose` string.

        Returns:
            str: A string representing the appropriate response based on the user's input.
        """
        purpose = args[1]
        action = args[-1]
        room = parser.tile_at(self.x, self.y)
        if purpose == "trade" and not self.is_selling:
            inventory = args[0]
        elif purpose == "pick-up":
            inventory = room.inventory
        elif purpose in [Armor.__name__, Curse.__name__, Healer.__name__, Weapon.__name__]:
            category = globals()[purpose]
            inventory = self.sort_items_by_category(self.inventory, category)
        else:
            inventory = self.inventory

        if action in ('q', 'exit', 'no'):
            return "Ok. Action cancelled."
        try:
            item_index = int(action)
            choice = inventory[item_index - 1]
            return self.show_appropriate_answer(choice, purpose)
        except Exception as e:
            return f"{e}"

    def show_appropriate_answer(self, choice, purpose):
        room = parser.tile_at(self.x, self.y)
        match purpose:
            case "my-inventory":
                return f"{choice}: \n{choice.description}"
            case "trade" if self.is_selling:
                self.items_swapper(self, room.talker, choice, purpose)
                self.is_selling = False
                return f"Bye {choice.name}!"
            case "trade" if not self.is_selling:
                self.items_swapper(room.talker, self, choice, purpose)
                return f"Good! Now {choice.name} is yours!"
            case "pick-up":
                self.items_swapper(room, self, choice, purpose)
                return f"{choice.name}: taken."
            case "drop":
                self.items_swapper(self, room, choice, purpose)
                return f"{choice.name}: dropped."
            case "Curse":
                return self.check_enemy_hp(room.enemy, self.cast_curse(room.enemy, choice))
            case "Healer":
                self.hp += choice.heal
                self.inventory.remove(choice)
                return f"You use {choice.name}. You now have {self.hp} HP remaining."
            case _:
                return

    def items_swapper(self, giver, receiver, item, purpose):
        if purpose == "trade" and receiver == self:
            if item.value > receiver.gold:
                return "<< You don't have enough cash. >>"
            giver.gold += item.value
            receiver.gold -= item.value
        giver.inventory.remove(item)
        receiver.inventory.append(item)
        giver.sort_inventory()
        receiver.sort_inventory()

    def get_or_drop_item(self, giver, receiver, target, purpose):
        if target in "all":
            return self.get_or_drop_all(giver, receiver, purpose)

        for item in giver.inventory:
            if target in item.name.lower():
                self.items_swapper(giver, receiver, item, "get-drop")
                if purpose == "get":
                    return f"{item.name}: taken."
                else:
                    return f"{item.name}: dropped."
        return(f"You can't see any {target} here")

    def get_or_drop_all(self, giver, receiver, purpose):
        response = ""
        print(giver.inventory)
        for item in giver.inventory:
            if purpose == "get":
                response += f"{item.name}: taken.\n"
            else:
                response += f"{item.name}: dropped.\n"
        receiver.inventory.extend(giver.inventory)
        giver.inventory.clear()
        if response == "":
            return f"There is nothing to {purpose}."
        else:
            return response

    def look(self, room):
        response = room.description
        for item in room.inventory:
            response += f"\nThere is a {item.name} here."
        if room.talker:
            response += f"\nThere is {room.talker.name} here."
        if room.enemy and room.enemy.is_alive():
            response += f"\nThere is a {room.enemy.name} here, willing to kill you."
        if room.enemy and not room.enemy.is_alive():
            response += f"\nThere the corpse of a {room.enemy.name} here."
        return response

    # -------------------------------------------------------------------------|
    # INFO --------------------------------------------------------------------|
    # -------------------------------------------------------------------------|

    def diagnose(self):
        room = parser.tile_at(self.x, self.y)
        return (
            f"> Level : {self.lvl}\n"
            f"> HP : {self.hp}/{self.max_hp}\n"
            f"> Mana : {self.mana}/{self.max_mana}\n"
            f"> § : {self.gold}\n"
            f"> XP : {self.xp}/{self.xp_modifier}\n"
            f"> Weapon equipped : {self.current_weapon}\n"
            f"> Turn : {self.turn}\n"
            f"> Location : {self.x}.{self.y} - {room.name}\n"
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

    def drop_all_get_all(self, receiver, giver):
        room = parser.tile_at(self.x, self.y)
        for _, item in enumerate(giver.inventory, 0):
            receiver.inventory.extend(giver.inventory)
            giver.inventory = []
            if receiver is self:
                print(f"{item.name}: taken.")
            if receiver is room:
                print(f"{item.name}: dropped.")

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

