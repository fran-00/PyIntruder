import re
import random

from engine.utils.combat_system import Combat
from entities.templates import Armor, Curse, Healer, ManaRecharger, MissionRelatedItem, Weapon, Trader
from entities.factory import ItemsFactory
import world.parser as parser
import world.tiles as world


class Inventory:
    def __init__(self):
        self.player = None
        self.owner = None
        self.room = None
        self.purpose = None
        self.action = None

    def show_instructions(func):
        def wrapper(*args):
            player = args[1] # The first argument of collect_request_data is self!
            purpose = args[3]
            print(purpose)
            response = ""
            match purpose:
                case "player-inventory":
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
                case "curse":
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

    @show_instructions
    def collect_request_data(self, *args):
        self.player = args[0]
        self.owner = args[1]
        self.owner.inventory.sort(key=lambda x: (x.__class__.__name__, x.name.lower()))
        self.purpose = args[2]
        self.category = args[3]
        if self.category is None:
            return self.show_inventory()
        return self.show_inventory_subset()

    def show_inventory(self):
        if self.owner.inventory == []:
            return self.handle_if_inventory_is_empty()
        response = ""
        index = 1
        for parent in [Armor, Curse, Healer, ManaRecharger, MissionRelatedItem, Weapon]:
            words = re.findall('[A-Z][^A-Z]*', parent.__name__)
            parent_name = ' '.join(words) + "s" + ":"
            items_subset = sorted([item for item in self.owner.inventory if isinstance(item, parent)], key=lambda item: item.name.lower())

            if items_subset:
                response += f"<p style='margin: 5px 0; color: #1296d3;'>{parent_name}</p>"

            for _, item in enumerate(items_subset, index):
                response += f"<p><span style='color: #1296d3;'>{index}.</span> - <b>{item}</b></p>"
                index += 1
        return response

    def show_inventory_subset(self):
        if self.category in [Armor.__name__, Curse.__name__, Healer.__name__, ManaRecharger.__name__, MissionRelatedItem.__name__, Weapon.__name__]:
            category = globals()[self.category]
            items_subset = sorted([item for item in self.owner.inventory if isinstance(item, category)], key=lambda item: item.name.lower())
            if items_subset == []:
                return self.handle_if_inventory_is_empty()
            response = ""
            index = 1
            for _, item in enumerate(items_subset, index):
                response += f"<p><span style='color: #1296d3;'>{index},</span> <b>{item}</b></p>"
                index += 1
        return response

    def handle_if_inventory_is_empty(self):
        match self.purpose:
            case "player-inventory":
                return f"Your inventory is empty! You have {self.player.gold} §."
            case "pick-up":
                return "There is nothing to pick up.", None
            case "drop":
                return "You don't have anything to drop.", None
            case "heal":
                return "You don't have anything to cure yourself with.", None
            case "curse":
                return "You don't have any curse.", None
            case "trade-player":
                return "You don't have anything to sell!", None
            case "trade-trader":
                return "Out of stock! Come back later!", None
            case _:
                return "Error"

    def choose_item(self, *args):
        self.player = args[0]
        self.room = parser.tile_at(self.player.x, self.player.y) # This must be set here: when commands calls choose_item a new instance of this class is created
        self.owner = args[1]
        self.owner.inventory.sort(key=lambda x: (x.__class__.__name__, x.name.lower()))
        self.purpose = args[2]
        self.category = args[3]
        action = args[-1]
        inventory = self.choose_queued_inventory()
        if action in ('q', 'exit', 'no'):
            return "Ok. Action cancelled."
        try:
            item_index = int(action)
            choice = inventory[item_index - 1]
            return self.show_appropriate_answer(choice)
        except Exception as e:
            return f"{e}"

    def choose_queued_inventory(self):
        if self.purpose == "trade" and not self.player.is_selling:
            inventory = self.room.talker.inventory
        elif self.purpose == "pick-up":
            inventory = self.room.inventory
        elif self.purpose in [Armor.__name__, Curse.__name__, Healer.__name__, ManaRecharger.__name__, MissionRelatedItem.__name__, Weapon.__name__]:
            category = globals()[self.purpose]
            inventory = sorted([item for item in self.owner.inventory if isinstance(item, category)], key=lambda item: item.name.lower())
        else:
            inventory = self.player.inventory
        return inventory

    def show_appropriate_answer(self, choice):
        if choice.marketable == False:
            return f"You can't sell {choice.name}!"
        match self.purpose:
            case "my-inventory":
                return f"{choice}: {choice.description}"
            case "trade" if self.player.is_selling:
                Inventory.items_swapper(self.splayer, self.room.talker, choice, self.purpose)
                return f"Bye {choice.name}!"
            case "trade" if not self.player.is_selling:
                Inventory.items_swapper(self.room.talker, self.player, choice, self.purpose)
                return f"Good! Now {choice.name} is yours!"
            case "pick-up":
                Inventory.items_swapper(self.room, self.player, choice, self.purpose)
                return f"{choice.name}: taken."
            case "drop":
                Inventory.items_swapper(self.player, self.room, choice, self.purpose)
                return f"{choice.name}: dropped."
            case "curse":
                return Combat.check_enemy_hp(self.player, self.room.enemy, Combat.curse_command_handler(self.player, room.enemy, choice))
            case "heal":
                return self.player.heal_command_handler(choice)
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

    @staticmethod
    def initialize_trade(*args):
        talker = args[1]
        if talker and isinstance(talker, Trader):
            Inventory.fill_trader_inventory(talker)
            return "<p>(B)uy, (S)ell or (Q)uit?</p>"
        elif talker:
            return f"{talker.name} doesn't want to trade.", None
        else:
            return "There is no one to trade with.", None

    @staticmethod
    def trading_mode(*args):
        player = args[0]
        trader = args[1]
        action = args[-1]
        match action:
            case "b":
                trader.is_selling = True
                player.is_selling = False
                return Inventory.check_someone_inventory(trader, "trade-trader")
            case "s":
                trader.is_selling = False
                player.is_selling = True
                return Inventory.check_someone_inventory(player, "trade-player")
            case "q":
                return "Come back when you want to trade!", None
            case _:
                return "Invalid choice, try again.", None

    @staticmethod
    def fill_trader_inventory(talker):
        items_list = ItemsFactory().get_entities_list(talker.type)
        if not talker.inventory:
            talker.inventory += random.sample(items_list, k=10)
