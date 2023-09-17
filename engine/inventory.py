import re
from dataclasses import dataclass

from entities.templates import Armor, Curse, Healer, ManaRecharger, MissionRelatedItem, Weapon
import world.parser as parser
import world.tiles as world


@dataclass
class Inventory:

    @staticmethod
    def trading_mode(*args):
        player = args[0]
        trader = args[1]
        action = args[-1]
        match action:
            case "b":
                return Inventory.check_player_inventory(trader, "trade-trader")
            case "s":
                player.is_selling = True
                return Inventory.check_trader_inventory(player, "trade-player")
            case "q":
                return "Come back when you want to trade!", None
            case _:
                return "Invalid choice, try again.", None

    def show_instructions(func):
        def wrapper(*args):
            player = args[0]
            purpose = args[2]
            match purpose:
                case "my-inventory":
                    response = f"<p>Your wealth: {player.gold} §</p>"
                    return func(*args) + response
                case "trade-trader":
                    response = f"What do you want to buy? You have {player.gold} §."
                case "trade-player":
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
    def check_player_inventory(player, purpose):
        inventory = player.inventory
        inventory.sort(key=lambda x: (x.__class__.__name__, x.name.lower()))
        if purpose in [Armor.__name__, Curse.__name__, Healer.__name__, ManaRecharger.__name__,  MissionRelatedItem.__name__, Weapon.__name__]:
            return Inventory.handle_showing_only_an_inventory_subset(player, purpose)
        elif inventory == []:
            Inventory.check_inventory_call_purpose(player, purpose)
        else:
            return Inventory.show_inventory(player, inventory, purpose)

    @staticmethod
    def handle_showing_only_an_inventory_subset(player, purpose):
        category = globals()[purpose]
        items_subset = Inventory.sort_items_by_category(player.inventory, category)
        if items_subset == []:
            return f"You don't have any {purpose} with you", None
        else:
            return Inventory.show_inventory(player, player.inventory, purpose)
    
    @staticmethod
    def check_inventory_call_purpose(player, purpose):
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

    @staticmethod
    def check_trader_inventory(trader, purpose):
        inventory = trader.inventory
        inventory.sort(key=lambda x: (x.__class__.__name__, x.name.lower()))
        if purpose in [Armor.__name__, Curse.__name__, Healer.__name__, ManaRecharger.__name__,  MissionRelatedItem.__name__, Weapon.__name__]:
            category = globals()[purpose]
            items_subset = Inventory.sort_items_by_category(
                trader.inventory, category)
            if items_subset == []:
                return f"You don't have any {purpose} with you", None
            else:
                return Inventory.show_inventory(trader, inventory, purpose)
        elif inventory == []:
            match purpose:
                case "my-inventory":
                    return "Your inventory is empty!", None
                case "trade" if trader == "trade-player":
                    return "You don't have anything to sell!", None
                case "trade" if trader == "trade-trader":
                    return "Out of stock! Come back later!", None
                case "pick-up":
                    return "There is nothing to pick up.", None
                case "drop":
                    return "You don't have anything to drop.", None
        else:
            return Inventory.show_inventory(trader, inventory, purpose)

    @show_instructions
    def show_inventory(shower, inventory, purpose):
        if purpose in [Armor.__name__, Curse.__name__, Healer.__name__, ManaRecharger.__name__, MissionRelatedItem.__name__, Weapon.__name__]:
            return Inventory.compose_string_with_inventory_subset(shower, purpose)
        else:
            return Inventory.compose_string_with_inventory_sorted_by_category(inventory, purpose)
    
    @staticmethod
    def compose_string_with_inventory_subset(player, purpose):
        response = ""
        category = globals()[purpose]
        items_subset = Inventory.sort_items_by_category(player.inventory, category)
        if items_subset != []:
            index = 1
            for _, item in enumerate(items_subset, index):
                response += f"<p><span style='color: #1296d3;'>{index},</span> <b>{item}</b></p>"
                index += 1
        return response

    @staticmethod
    def compose_string_with_inventory_sorted_by_category(inventory, purpose):
        index = 1
        response = ""
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
    def choose_item(player, purpose, action):
        room = parser.tile_at(player.x, player.y)
        inventory = Inventory.choose_queued_inventory(player, room, purpose)

        if action in ('q', 'exit', 'no'):
            return "Ok. Action cancelled."
        try:
            item_index = int(action)
            choice = inventory[item_index - 1]
            return Inventory.show_appropriate_answer(choice, purpose)
        except Exception as e:
            return f"{e}"

    @staticmethod
    def choose_queued_inventory(player, room, purpose):
        if purpose == "trade" and not player.is_selling:
            inventory = room.talker.inventory
        elif purpose == "pick-up":
            inventory = room.inventory
        elif purpose in [Armor.__name__, Curse.__name__, Healer.__name__, ManaRecharger.__name__, MissionRelatedItem.__name__, Weapon.__name__]:
            category = globals()[purpose]
            inventory = Inventory.sort_items_by_category(player.inventory, category)
        else:
            inventory = player.inventory
        return inventory

    @staticmethod
    def show_appropriate_answer(player, choice, purpose):
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
        if purpose == "trade":
            if item.value > receiver.gold:
                return "<< You don't have enough cash. >>"
            giver.gold += item.value
            receiver.gold -= item.value
        giver.inventory.remove(item)
        receiver.inventory.append(item)