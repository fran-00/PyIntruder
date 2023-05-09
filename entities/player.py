import random

from .templates import Armor, Curse, Healer, ManaRecharger, MissionRelatedItem, Weapon
from .factory import Factory

import world.parser as parser
import world.tiles as world


class Player:
    def __init__(self):
        self.name = 'Your Name Here'
        self.x = parser.start_tile_location[0]
        self.y = parser.start_tile_location[1]

        self.inventory = [Factory().veridical,
                          Factory().wire,
                          Factory().fungine_armor,
                          Factory().ats]
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
        """Update Player's coordinates within the game map.

        Parameters
        ----------
            dx : int
                The change in the x coordinate.
            dy : int
                The change in the y coordinate.
        """
        self.x += dx
        self.y += dy

    def get_coordinates(self, dx, dy):
        self.previous_x = self.x
        self.previous_y = self.y
        self.move(dx=dx, dy=dy)

    def move_north(self):
        self.get_coordinates(0, -1)

    def move_south(self):
        self.get_coordinates(0, 1)

    def move_east(self):
        self.get_coordinates(1, 0)

    def move_west(self):
        self.get_coordinates(-1, 0)

    # -------------------------------------------------------------------------|
    # COMBAT ------------------------------------------------------------------|
    # -------------------------------------------------------------------------|

    def best_weapon(self):
        """Find the best weapon in the player's inventory and return it.

        Returns
        -------
        best_weapon : Weapon
            The weapon in the player's inventory with higher damage attribute
        None
            The player has no weapons.
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
        """Attempt to attack an enemy in the current room with the best
        available weapon.

        Returns
        -------
        str
            Return the result of calling calculate_attack_precision() with
            arguments for the enemy, weapon, and a message about the attack
            attempt.
            If the player has no weapon, return a message stating this.
        None
            If there is no living enemy in the room, return None.
        """
        weapon = self.best_weapon()
        room = parser.tile_at(self.x, self.y)
        enemy = room.enemy
        response = ""

        if weapon is None:
            return "You don't have any weapon with you."

        if enemy is None or not enemy.is_alive():
            return

        response += f"You try to hit {enemy.name} with {weapon.name}!"
        return self.calculate_attack_precision(enemy, weapon, response)

    def calculate_attack_precision(self, enemy, weapon, response):
        """Calculate attack precision and damage multiplier based on a random integer.
        
        Parameters
        ----------
        enemy : Enemy
            An Enemy class instance alive in the current room.
        weapon : Weapon
            Best player's weapon, if any.
        response : str
            A string to add to the response.
        
        Returns
        -------
        func
            Call check_enemy_hp() passing enemy and response string as arguments
        """
        precision = random.randint(1, 20)
        match precision:
            case 20:
                damage_multiplier = 2
                response += (
                    f"\nCritical hit! "
                    f"You deal {weapon.damage * damage_multiplier} DMG!"
                )
            case 17 | 18 | 19:
                damage_multiplier = 1.5
                response += (
                    f"\nGood hit! "
                    f"You deal {weapon.damage * damage_multiplier} DMG!"
                )
            case 3 | 2 | 1:
                response += "\nMissed!"
                return response
            case _:
                damage_multiplier = 1
                response += f"\nYou deal {weapon.damage} DMG!"

        enemy.hp -= weapon.damage * damage_multiplier
        return self.check_enemy_hp(enemy, response)

    def check_enemy_hp(self, enemy, response):
        """Check the HP of an enemy and responds accordingly.

        Parameters
        ----------
        enemy : Enemy
            An instance of Enemy class representing the enemy being checked.
        response : str
            The current response string that is being built.

        Returns
        -------
        str
            The updated response string after checking the enemy's HP.
        """
        if not enemy.is_alive():
            response += f"\nYEAH! You killed it!"
            response += self.add_xp(enemy)
            loot = random.randint(10, 200)
            self.gold += loot
            response += f"\n{enemy.name} lost his booty. Now {loot} § are yours!"

        else:
            response += f"\n{enemy.name} has {enemy.hp} HP remaining."
        return response

    def add_xp(self, enemy):
        """Calculate the earned XP points from killing an enemy, update Player
        level if necessary and return the response string for the XP gain.

        Parameters
        ----------
        enemy : Enemy
            An instance of Enemy class representing killed enemy.

        Returns
        -------
        str
            The updated response string after earning XP.
        """
        xp_earned = (enemy.damage // 2)
        response = f"\nYou earned {xp_earned} XP!"
        self.xp += xp_earned
        if self.xp >= self.xp_modifier:
            response += self.level_up()
        return response

    def level_up(self):
        """Increase Player level and updates the maximum health and mana points.

        Returns
        -------
        str
            A string indicating the new player level.
        """
        self.xp_modifier *= 1.1
        self.lvl += 1
        self.max_hp *= 1.1
        self.hp = self.max_hp
        self.max_mana *= 1.1
        self.mana = self.max_mana
        return f"You leveled up! You are now at {self.lvl} LVL."

    def cast_curse(self, enemy, choice):
        """Cast a curse on an enemy.

        Called by show_appropriate_answer() method if purpose argument is
        "Curse". If there is not enough mana to cast the spell, return a string
        indicating so. Otherwise, subtract the mana cost from the caster's mana
        pool and the curse's damage from the target's hp.

        Parameters
        ----------
        enemy : Enemy
            The enemy in the current room.
        choice : Curse
            The choosen curse returned by choose_item() method.

        Returns
        -------
        str
            Return a formatted string indicating name of the spell cast,
            damage dealt and remaining mana.
        """
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
        """Sorts the inventory in-place based on the item class name and item name."""
        self.inventory.sort(key=lambda x: (x.__class__.__name__, x.name))
        return

    def trading_mode(self, *args):
        """Enter trading mode with a non-player character.
        
        Parameters
        ----------
        *args
            Accepts any number of arguments.
            *args[-1] (str): [Required] User's action
        Returns
        -------
        str
            if action is "B" or "S", return the result of calling
            check_inventory() passing as argument player's inventory
            (if selling) or trader's inventory (if buying).
        tuple : str, None
            if action is q or is not recognizedm return a tuple with a
            message and None value to break play() loop.
        """
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
        """Decorator: add a response string to decorated function, based on its argument.

        The wrapper function determines the functionality based on the second
        argument of the decorated function, "purpose": a message is
        created and appended to the result of the called function.
        If no matching value is encountered, no message is added.

        Parameters
        ----------
        func : function
            The function to be decorated. It must have a string argument 
            with the string "purpose".

        Returns
        -------
        function
            A new function that wraps the given function with added functionality.
        """
        def wrapper(self, *args):
            purpose = args[1]
            match purpose:
                case "my-inventory":
                    response = f"Your wealth: {self.gold} §"
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
        """Check if inventory contains any items or items of a specified category

        Parameters
        ----------
        *args
            A tuple of positional arguments.
            *args[0] (list): [Required] The inventory to show.
            *args[1] (str): [Required] The purpose of the inventory check.

        Returns
        -------
        tuple
            If no items are found, a tuple that contains a string with 
            informative message and None value
        str
            If items are found, call show_inventory() method passing inventory
            and purpose as arguments
        """
        inventory = args[0]
        purpose = args[1]
        
        if purpose in [Armor.__name__, Curse.__name__, Healer.__name__,  MissionRelatedItem.__name__, Weapon.__name__]:
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
        """Display an inventory based on purpose.

        Parameters
        ----------
        *args
            Arguments to customize the display of an inventory:
            *args[0]: [Required] The inventory to show.
            *args[1]: [Required] The purpose of the retrieval.
        Returns
        -------
        response : str
            A formatted string containing the inventory.
        """
        inventory = args[0]
        purpose = args[1]
        index = 1
        response = ""
        
        if purpose in [Armor.__name__, Curse.__name__, Healer.__name__, MissionRelatedItem.__name__, Weapon.__name__]:
            category = globals()[purpose]
            items_subset = self.sort_items_by_category(self.inventory, category)
            if items_subset != []:
                for _, item in enumerate(items_subset, index):
                    response += f"{index}. {item}\n"
                    index += 1
        else:
            for parent in [Armor, Curse, Healer, MissionRelatedItem, Weapon]:
                items_subset = self.sort_items_by_category(inventory, parent)

                if items_subset:
                    response += f">> {parent.__name__.upper()}S:\n"

                for _, item in enumerate(items_subset, index):
                    if purpose in ["trade"]:
                        response += f"{index}. - {item} - {item.value}§\n"
                    else:
                        response += f"> {item}\n"
                    index += 1
        return response

    def sort_items_by_category(self, inventory, category):
        return sorted([item for item in inventory if isinstance(item, category)], key=lambda item: item.name.lower())

    def choose_item(self, *args):
        """Selects an item from the inventory based on the user's input.

        Parameters
        ----------
        *args
            The arguments to customize the behavior of the method:
            *args[0]: The inventory to use for trade purposes or None
            *args[1]: The purpose of the item selection
            *args[-1]: The action to perform

        Returns
        -------
        str
            Call show_appropriate_answer() passing choosen item and purpose
            as arguments. If action is cancelled, return a message.
        
        Raises
        ------
        Exception
            If action is not a valid number or if choice index is out of range
        """
        purpose = args[1]
        action = args[-1]
        room = parser.tile_at(self.x, self.y)
        if purpose == "trade" and not self.is_selling:
            inventory = args[0]
        elif purpose == "pick-up":
            inventory = room.inventory
        elif purpose in [Armor.__name__, Curse.__name__, Healer.__name__, MissionRelatedItem.__name__, Weapon.__name__]:
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
        """Displays the appropriate answer for the given choice and purpose.

        Parameters
        ----------
        choice : Item
            The selected item
        purpose : str
            The purpose of the selection

        Returns
        -------
        str
            The appropriate string response for the selected `choice` and
            `purpose` obtained from item_swapper() if manipulating items,
            from check_enemy_hp() if fighting or from heal() if player wants
            to consume an Healer.
        """
        room = parser.tile_at(self.x, self.y)
        if choice.marketable == False:
            return f"You can't sell {choice.name}!"
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
                return self.heal_command_handler(choice)
            case _:
                return

    def heal_command_handler(self, choice):
        """Heal Player using chosen item and remove it from the inventory.

        Parameters
        ----------
        choice : Healer
            The selected item to use for healing. It must have a 'heal' attribute.

        Returns
        -------
        str
            A string providing name of the item used and remaining HP.
        """
        if (choice.heal + self.hp) > self.max_hp:
            self.hp = self.max_hp
        else: 
            self.hp += choice.heal
        self.inventory.remove(choice)
        self.sort_inventory()
        return f"You use {choice.name}. You now have {self.hp} HP remaining."

    def items_swapper(self, giver, receiver, item, purpose):
        """Moves items between inventories of two Entities or buys/sells items.
        Call sort_inventory method on both Entities when done.

        Parameters
        ----------  
        giver
            The player instance that is giving the item.
        receiver
            The player instance that is receiving the item.
        item
            The item being transferred or bought/sold.
        purpose
            A string that specifies the purpose of the transfer. It can have two possible values: 'trade' (when the characters are trading items) or 'buy_sell' (when one character is buying and the other is selling).

        Returns
        -------
        str 
            String that warns if player has no gold. 
        None
            In any other case.
        """
        if purpose == "trade" and receiver == self:
            if item.value > receiver.gold:
                return "<< You don't have enough cash. >>"
            giver.gold += item.value
            receiver.gold -= item.value
        giver.inventory.remove(item)
        receiver.inventory.append(item)
        giver.sort_inventory()
        receiver.sort_inventory()

    def get_and_drop_command_handler(self, giver, receiver, target, purpose):
        if target in "all":
            return self.get_or_drop_all(giver, receiver, purpose)

        for item in giver.inventory:
            if target in item.name.lower():
                self.items_swapper(giver, receiver, item, "get-drop")
                receiver.sort_inventory()
                giver.sort_inventory()
                if purpose == "get":
                    return f"{item.name}: taken."
                else:
                    return f"{item.name}: dropped."
        # TODO: a different response should be shown if the target is present
        # but cannot be picked up, for example in the case of an NPC, an enemy
        # or a heavy object. 
        # The answer in these cases should be "Not bloody likely."
        return(f"You can't see any {target} here")

    def get_or_drop_all(self, giver, receiver, purpose):
        """Takes all items from giver's inventory, add them to receiver's inventory
        and show appropriate message based on purpose.
        
        Parameters
        ----------
        giver : Player or Room
            The class who gives items.
        receiver : Player or Room
            The class who receives items.
        purpose : str)
            The purpose of the transfer operation. 
            Must be either "get" or "drop".

        Returns
        -------
        str
            A response indicating the status of the transfer operation.
            If there are no items to transfer, "There is nothing to [purpose]."
            Otherwise, a string with the names of the transferred items and 
            the operation (taken/dropped).

        """
        response = ""
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

    # -------------------------------------------------------------------------|
    # INFO --------------------------------------------------------------------|
    # -------------------------------------------------------------------------|

    def diagnose_command_handler(self):
        """Returns a formatted string with the player's current status information."""
        room = parser.tile_at(self.x, self.y)
        return (
            f"> Level : {self.lvl}\n"
            f"> HP : {self.hp}/{self.max_hp}\n"
            f"> Mana : {self.mana}/{self.max_mana}\n"
            f"> § : {self.gold}\n"
            f"> XP : {self.xp}/{self.xp_modifier}\n"
            f"> Weapon equipped : {self.current_weapon}\n"
            f"> Turn : {self.turn}\n"
            f"> Location : {self.x}.{self.y} - {room.name}"
        )

    def show_map(self):
        """Print a visual representation of the world map and player's coordinates.

        The map is defined in the `world_dsl` funcion of `parser` module, and is
        parsed into a grid of string representations of the different types of
        map tiles. The `tile_type_dict` dictionary maps each tile type to its
        corresponding string representation. The map is printed row by row, with
        each tile represented by a string enclosed in vertical bars.
        
        FIXME: the map is currently printed in the terminal because it is shown
        truncated in the game window.
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
