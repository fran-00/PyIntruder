import re
import random
from dataclasses import dataclass

from entities.factory import ItemsFactory
from entities.templates import Armor, Curse, Healer, ManaRecharger, MissionRelatedItem, Weapon, Trader
import world.parser as parser
import world.tiles as world


class Inventory:
    def __init__(self):
        self.player = None
        self.npc = None
        self.scope = None
        self.action = None

    @staticmethod
    def show_generic_inventory(inventory, category):
        inventory.sort(key=lambda x: (x.__class__.__name__, x.name.lower()))
        response = ""
        if inventory == []:
            response += "This inventory is empty"
        else:
            index = 1
            for item_category in [Armor, Curse, Healer, ManaRecharger, MissionRelatedItem, Weapon]:
                words = re.findall('[A-Z][^A-Z]*', item_category.__name__)
                parent_name = ' '.join(words) + "s" + ":"
                items_subset = Inventory.sort_items_by_category(inventory, item_category)

                if items_subset:
                    response += f"<p style='margin: 5px 0; color: #1296d3;'>{parent_name}</p>"

                for _, item in enumerate(items_subset, index):
                    response += f"<p><span style='color: #1296d3;'>{index}.</span> - <b>{item}</b></p>"
                    index += 1
        return response

    @staticmethod
    def check_someone_inventory(*args):
        someone = args[0]
        purpose = args[1]
        inventory = someone.inventory
        inventory.sort(key=lambda x: (x.__class__.__name__, x.name.lower()))
        if purpose in [Armor.__name__, Curse.__name__, Healer.__name__, ManaRecharger.__name__,  MissionRelatedItem.__name__, Weapon.__name__]:
            return Inventory.handle_showing_only_an_inventory_subset(someone, purpose)
        elif inventory == []:
            Inventory.handle_if_inventory_is_empty(someone, purpose)
        else:
            return Inventory.show_inventory(someone, inventory, purpose)

    @staticmethod
    def handle_showing_only_an_inventory_subset(player, purpose):
        category = globals()[purpose]
        items_subset = Inventory.sort_items_by_category(player.inventory, category)
        if items_subset == []:
            return f"You don't have any {purpose} with you", None
        else:
            return Inventory.show_inventory(player, player.inventory, purpose)
    
    @staticmethod
    def handle_if_inventory_is_empty(player, purpose):
        # FIXME: mostra sempre "invalid literal for int() with base 10: 'pick up'""
        # perché viene eseguita choose_item immediatamente dopo anche quando non
        # dovrebbe. In pratica il loop non viene interrotto correttamenre
        match purpose:
            case "my-inventory":
                return f"Your inventory is empty! You have {player.gold} §.", None
            case "trade-player":
                return "You don't have anything to sell!", None
            case "trade-trader":
                return "Out of stock! Come back later!", None
            case "pick-up":
                return "There is nothing to pick up.", None
            case "drop":
                return "You don't have anything to drop.", None
            case _:
                return "Error"

    @staticmethod
    def show_inventory(someone, inventory, purpose):
        if purpose in [Armor.__name__, Curse.__name__, Healer.__name__, ManaRecharger.__name__, MissionRelatedItem.__name__, Weapon.__name__]:
            return Inventory.compose_string_with_inventory_subset(someone, purpose)
        else:
            return Inventory.compose_string_with_inventory_sorted_by_category(someone.inventory, purpose)
    
    @staticmethod
    def compose_string_with_inventory_subset(someone, purpose):
        response = ""
        category = globals()[purpose]
        items_subset = Inventory.sort_items_by_category(someone.inventory, category)
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
    def choose_item(*args):
        player = args[0]
        # -This is the only way to use this method for many purposes because
        # if used for trading or gathering it has a different number of arguments
        purpose = args[-3]
        action = args[-1]
        room = parser.tile_at(player.x, player.y)
        inventory = Inventory.choose_queued_inventory(player, room, purpose)

        if action in ('q', 'exit', 'no'):
            return "Ok. Action cancelled."
        try:
            item_index = int(action)
            choice = inventory[item_index - 1]
            return Inventory.show_appropriate_answer(player, choice, purpose)
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
                return "Problems"

    @staticmethod
    def items_swapper(giver, receiver, item, purpose):
        if purpose == "trade":
            if item.value > receiver.gold:
                return "<< You don't have enough cash. >>"
            giver.gold += item.value
            receiver.gold -= item.value
        giver.inventory.remove(item)
        receiver.inventory.append(item)

    # @staticmethod
    # def trading_mode(*args):
    #     player = args[0]
    #     trader = args[1]
    #     action = args[-1]
    #     match action:
    #         case "b":
    #             trader.is_selling = True
    #             player.is_selling = False
    #             return Inventory.check_someone_inventory(trader, "trade-trader")
    #         case "s":
    #             trader.is_selling = False
    #             player.is_selling = True
    #             return Inventory.check_someone_inventory(player, "trade-player")
    #         case "q":
    #             return "Come back when you want to trade!", None
    #         case _:
    #             return "Invalid choice, try again.", None

    # @staticmethod
    # def initialize_trade(*args):
    #     talker = args[1]
    #     if talker and isinstance(talker, Trader):
    #         Inventory.fill_trader_inventory(talker)
    #         sentence = talker.get_random_opening_sentence(f"{talker.name}")
    #         # FIXME: sentence is not shown
    #         return f"<p>{sentence}<p><p>(B)uy, (S)ell or (Q)uit?</p>"
    #     elif talker:
    #         return f"{talker.name} doesn't want to trade.", None
    #     else:
    #         return "There is no one to trade with.", None

    # @staticmethod
    # def fill_trader_inventory(talker):
    #     items_list = ItemsFactory().get_entities_list(talker.type)
    #     if not talker.inventory:
    #         talker.inventory += random.sample(items_list, k=10)

    # def show_instructions(func):
    #     def wrapper(*args):
    #         player = args[0]
    #         purpose = args[2]
    #         match purpose:
    #             case "my-inventory":
    #                 response = f"<p>Your wealth: {player.gold} §</p>"
    #                 return func(*args) + response
    #             case "trade-trader":
    #                 response = f"What do you want to buy? You have {player.gold} §."
    #             case "trade-player":
    #                 response = "What do you want to sell?"
    #             case "pick-up":
    #                 response = "What do you want to pick up?"
    #             case "drop":
    #                 response = "What do you want to drop?"
    #             case "Curse":
    #                 response = (
    #                     f"<p>Ok, what curse do you want to cast?</p>"
    #                     f"<p>You have {player.mana} Mana.</p>"
    #                 )
    #             case "Healer":
    #                 response = (
    #                     f"<p>Your health is {player.hp}/{player.max_hp}.</p>"
    #                     "<p>What do you want to treat yourplayer with?</p>"
    #                 )
    #         response += "<p>Choose an item or press Q to quit.</p>"
    #         return func(*args) + response
    #     return wrapper
