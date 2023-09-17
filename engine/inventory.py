import re
from dataclasses import dataclass

from entities.templates import Armor, Curse, Healer, ManaRecharger, MissionRelatedItem, Weapon
import world.parser as parser
import world.tiles as world


@dataclass
class Inventory:

    @staticmethod
    def trading_mode(*args):
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
        player = args[0]
        talker = args[1]
        action = args[-1]
        match action:
            case "b":
                return Inventory.check_inventory(talker, "trade")
            case "s":
                player.is_selling = True
                return Inventory.check_inventory(player, "trade")
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

        def wrapper(*args):
            print(*args)
            player = args[0]
            purpose = args[2]
            match purpose:
                case "my-inventory":
                    response = f"<p>Your wealth: {player.gold} §</p>"
                    return func(*args) + response
                case "trade" if not player.is_selling:
                    response = f"What do you want to buy? You have {player.gold} §."
                case "trade" if player.is_selling:
                    response = "What do you want to sell?"
                case "pick-up":
                    response = "What do you want to pick up?"
                case "drop":
                    response = "What do you want to drop?"
                case "Curse":
                    response = (
                        f"<p>Ok, what curse do you want to cast?</p>"
                        f"<p>You have {player.mana} Mana.</p>"
                    )
                case "Healer":
                    response = (
                        f"<p>Your health is {player.hp}/{player.max_hp}.</p>"
                        "<p>What do you want to treat yourplayer with?</p>"
                    )
            response += "<p>Choose an item or press Q to quit.</p>"
            return func(*args) + response
        return wrapper

    @staticmethod
    def check_inventory(*args):
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
        player = args[0]
        purpose = args[1]
        inventory = player.inventory
        inventory.sort(key=lambda x: (x.__class__.__name__, x.name.lower()))
        if purpose in [Armor.__name__, Curse.__name__, Healer.__name__, ManaRecharger.__name__,  MissionRelatedItem.__name__, Weapon.__name__]:
            category = globals()[purpose]
            items_subset = Inventory.sort_items_by_category(
                player.inventory, category)
            if items_subset == []:
                return f"You don't have any {purpose} with you", None
            else:
                return Inventory.show_inventory(player, inventory, purpose)
        elif inventory == []:
            match purpose:
                case "my-inventory":
                    return f"Your inventory is empty! You have {player.gold} §.", None
                case "trade" if player.is_selling:
                    return "You don't have anything to sell!", None
                case "trade" if not player.is_selling:
                    return "Out of stock! Come back later!", None
                case "pick-up":
                    return "There is nothing to pick up.", None
                case "drop":
                    return "You don't have anything to drop.", None
        else:
            return Inventory.show_inventory(player, inventory, purpose)

    @show_instructions
    def show_inventory(*args):
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
        purpose = args[2]
        index = 1
        response = ""

        if purpose in [Armor.__name__, Curse.__name__, Healer.__name__, ManaRecharger.__name__, MissionRelatedItem.__name__, Weapon.__name__]:
            category = globals()[purpose]
            items_subset = Inventory.sort_items_by_category(
                player.inventory, category)
            if items_subset != []:
                for _, item in enumerate(items_subset, index):
                    response += f"<p><span style='color: #1296d3;'>{index},</span> <b>{item}</b></p>"
                    index += 1
        else:
            for parent in [Armor, Curse, Healer, ManaRecharger, MissionRelatedItem, Weapon]:
                words = re.findall('[A-Z][^A-Z]*', parent.__name__)
                parent_name = ' '.join(words) + "s" + ":"
                items_subset = Inventory.sort_items_by_category(inventory, parent)

                if items_subset:
                    response += f"<p style='margin: 5px 0; color: #1296d3;'>{parent_name}</p>"

                for _, item in enumerate(items_subset, index):
                    if purpose in ["trade"]:
                        response += f"<p><span style='color: #1296d3;'>{index}.</span> - <b>{item}</b> - {item.value}§</p>"
                    else:
                        response += f"<p><span style='color: #1296d3;'>{index}.</span> - <b>{item}</b></p>"
                    index += 1
        return response

    @staticmethod
    def sort_items_by_category(inventory, category):
        return sorted([item for item in inventory if isinstance(item, category)], key=lambda item: item.name.lower())

    @staticmethod
    def choose_item(*args):
        """Select an item from the inventory based on the user's input.

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
        player = args[0]
        purpose = args[2]
        action = args[-1]
        room = parser.tile_at(player.x, player.y)
        
        if purpose == "trade" and not player.is_selling:
            inventory = room.talker.inventory
        elif purpose == "pick-up":
            inventory = room.inventory
        elif purpose in [Armor.__name__, Curse.__name__, Healer.__name__, ManaRecharger.__name__, MissionRelatedItem.__name__, Weapon.__name__]:
            category = globals()[purpose]
            inventory = Inventory.sort_items_by_category(player.inventory, category)
        else:
            inventory = player.inventory

        if action in ('q', 'exit', 'no'):
            return "Ok. Action cancelled."
        try:
            item_index = int(action)
            choice = inventory[item_index - 1]
            return Inventory.show_appropriate_answer(choice, purpose)
        except Exception as e:
            return f"{e}"

    @staticmethod
    def show_appropriate_answer(player, choice, purpose):
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
        room = parser.tile_at(player.x, player.y)
        if choice.marketable == False:
            return f"You can't sell {choice.name}!"
        match purpose:
            case "my-inventory":
                return f"{choice}: {choice.description}"
            case "trade" if player.is_selling:
                Inventory.items_swapper(player, room.talker, choice, purpose)
                player.is_selling = False
                return f"Bye {choice.name}!"
            case "trade" if not player.is_selling:
                Inventory.items_swapper(room.talker, player, choice, purpose)
                return f"Good! Now {choice.name} is yours!"
            case "pick-up":
                Inventory.items_swapper(room, player, choice, purpose)
                return f"{choice.name}: taken."
            case "drop":
                Inventory.items_swapper(player, room, choice, purpose)
                return f"{choice.name}: dropped."
            case "Curse":
                return player.check_enemy_hp(room.enemy, player.curse_command_handler(room.enemy, choice))
            case "Healer":
                return player.heal_command_handler(choice)
            case _:
                return

    @staticmethod
    def items_swapper(giver, receiver, item, purpose):
        """Move items between inventories of two Entities or buys/sells items.
        Call sort_inventory method on both Entities when done.

        Parameters
        ----------  
        giver
            The class that is giving the item (Player, NPC or MapTile subclass).
        receiver
            The class that is is receiving the item.
        item
            The item being transferred or bought/sold.
        purpose
            A string that specifies the purpose of the transfer. If purpose is
            'trade', remove gold from buyer's inventory and add it to seller's.

        Returns
        -------
        str 
            String that warns if player has no gold.
        None
            In any other case.
        """
        if purpose == "trade":
            if item.value > receiver.gold:
                return "<< You don't have enough cash. >>"
            giver.gold += item.value
            receiver.gold -= item.value
        giver.inventory.remove(item)
        receiver.inventory.append(item)