import random
import re

from .templates import Entity
from .factory import ItemsFactory as items

import world.parser as parser
import world.tiles as world
from engine.utils.combat_system import Combat
from engine.utils.inventory import Inventory
from gui.styles.decorators import *


class Player(Entity):
    def __init__(self):
        self.name = 'Your Name Here'
        self.x = parser.start_tile_location[0]
        self.y = parser.start_tile_location[1]

        self.inventory = [items().stygian_blue,
                          items().wire,
                          items().hyperbolic_orange,
                          items().ats,
                          items().specimen,
                          items().dialectic_draught]
        self.current_weapon = Combat.best_weapon(self.inventory)
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

    def is_alive(self):
        return self.hp > 0

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

    def level_up(self):
        """Increase Player level and updates the maximum health and mana points.

        Returns
        -------
        str
            A string indicating the new player level.
        """
        self.xp_modifier = round((100 + self.xp_modifier) * 1.1)
        self.lvl += 1
        self.max_hp = round(self.max_hp * 1.1)
        self.hp = self.max_hp
        self.max_mana = round(self.max_mana * 1.1)
        self.mana = self.max_mana
        return f"You leveled up! You are now at {self.lvl} LVL."

    def flee_from_fight(self):
        room = parser.tile_at(self.x, self.y)
        d20 = random.randint(1, 20)
        if d20 == 20:
            room.enemy.alive = False
            return "No need to do this. Enemy is dead!"
        if d20 <= 15 or d20 >= 20:
            return "You can't escape!"
        self.x = self.previous_x
        self.y = self.previous_y
        # FIXME: it doesn't work! Enemy still attacks because loop is
        # still running and an AttributeError is raised if attacking again
        # when you call tile_at method from parser:
        # parser.tile_at(self.previous_x, self.previous_y)
        return "You flee."

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
        return f"You use {choice.name}. You now have {self.hp} HP remaining."

    def diagnose_command_handler(self):
        """Return a formatted string with the player's current status information."""
        room = parser.tile_at(self.x, self.y)
        return (
            f"<b>Level</b> : {self.lvl}<br>"
            f"<b>HP</b> : {self.hp}/{self.max_hp}<br>"
            f"<b>Mana</b> : {self.mana}/{self.max_mana}<br>"
            f"<b>§</b> : {self.gold}<br>"
            f"<b>XP</b> : {self.xp}/{self.xp_modifier}<br>"
            f"<b>Weapon equipped</b> : {self.current_weapon}<br>"
            f"<b>Turn</b> : {self.turn}<br>"
            f"<b>Location</b> : {self.x}.{self.y} - {room.name}"
        )

    # -------------------------------------------------------------------------|
    # GET/ DROP----------------------------------------------------------------|
    # -------------------------------------------------------------------------|

    def get_and_drop_command_handler(self, giver, receiver, target, purpose):
        """Handle the logic of getting and dropping items between two entities.

        Parameters
        ----------
        giver : Player or MapTile subclass
            The entity that will be giving the item: Player if dropping,
            current room if getting.
        receiver : Player or MapTile subclass
            The entity that will be receiving the item: current room if dropping,
            Player if getting.
        target : str
            Name of the item to be picked up or dropped. Can be 'all' to pick/
            drop all items of the giver.
        purpose : str
            Purpose of the action which can be 'get' or 'drop'.

        Returns
        -------
        str
            If the target is 'all', return a string containing the status of the
            get/drop all operation, otherwise the string will indicate whether
            the specified item was successfully taken or dropped. 
            If the specified  item is not in the giver's inventory or it cannot
            be collected/dropped because is not an item but another kind of entity,
            return a string detailing the reason why it's not possible provided
            by show_why_is_not_collectable_or_droppable method.
        """
        if target == "all":
            return self.get_or_drop_all(giver, receiver, purpose)

        for item in giver.inventory:
            if self.match_target_name(target, item):
                Inventory.items_swapper(giver, receiver, item, "get-drop")
                return f"{item.name}: taken." if purpose == "get" else f"{item.name}: dropped."
        return self.show_why_is_not_collectable_or_droppable(target, purpose)
    
    def show_why_is_not_collectable_or_droppable(self, target, purpose):
        """Call two other methods to determine why an item cannot be collected or
        dropped.

        Parameters
        ----------
        target : str
            Name of the item which the player is trying to interact with.
        purpose: str
            Type of interaction, which can be 'get' or 'drop'.

        Returns
        -------
        str
            A string message indicating why the specified item cannot be
            collected or dropped by the player obtained by calling
            handle_when_item_cannot_be_picked_up and handle_when_item_cannot_be_dropped
            methods.
        """
        room = parser.tile_at(self.x, self.y)
        if purpose == "get":
            return self.handle_when_item_cannot_be_picked_up(target, room)
        elif purpose == "drop":
            return self.handle_when_item_cannot_be_dropped(target, room)

    def handle_when_item_cannot_be_picked_up(self, target, room):
        """Handle the logic of determining why an item cannot be picked up.

        Parameters
        ----------
        target : str
            Name of the item which the player is trying to interact with.
        room : MapTile subclass
            The room the player is currently in.

        Returns
        -------
        str
            A message indicating why the specified item cannot be picked up.
        """
        for entity in room.environment:
            if self.match_target_name(target, entity):
                return "Not bloody likely."
        for item in self.inventory:
            if self.match_target_name(target, item):
                return "You already have it..."
        if room.enemy and self.match_target_name(target, room.enemy):
            if room.enemy.is_alive():
                return "I don't know if you noticed, but it's trying to kill you..."
            else:
                return "The corpse is too heavy to carry."
        elif self.match_target_name(target, room):
            return "Are you sure you're okay?"
        else:
            return f"{target.capitalize()} is something I don't recognize."

    def handle_when_item_cannot_be_dropped(self, target, room):
        """Handle the logic of determining why an item cannot be dropped.

        Parameters
        ----------
        target : str
            Name of the item which the player is trying to interact with.
        room : MapTile subclass
            The room the player is currently in.

        Returns
        -------
        str
            A message indicating why the specified item cannot be dropped.
        """
        for entity in room.environment:
            if self.match_target_name(target, entity):
                return "How is this supposed to work?"
        for item in room.inventory:
            if self.match_target_name(target, item):
                return "You can't drop something you don't own."
        if self.match_target_name(target, room.enemy):
            return f"Hummm... Ok, {room.enemy.styled_name()}: dropped. Now what?"
        if self.match_target_name(target, room):
            return "I don't even know what to answer..."
        else:
            return f"{target.capitalize()} is something I don't recognize."

    def match_target_name(self, target, obj):
        """Determine if a given `target` string matches any part of a given
        object's name using re module.

        Parameters
        ----------
        target : str
            The target string to match.
        obj : Any
            The object to check for a name match.

        Returns
        -------
        bool
            True if a match is found, False otherwise.
        """
        return bool(
            obj
            and re.search(
                rf"\b\w*({''.join([f'{c}' for c in target])})\w*\b",
                obj.name.lower(),
            )
            and len(set(target).intersection(set(obj.name.lower()))) >= 3
        )

    def get_or_drop_all(self, giver, receiver, purpose):
        """Take all items from giver's inventory, add them to receiver's inventory
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
        response = "".join(
            f"{item.name}: taken."
            if purpose == "get"
            else f"{item.name}: dropped."
            for item in giver.inventory
        )
        receiver.inventory.extend(giver.inventory)
        giver.inventory.clear()
        return response or f"There is nothing to {purpose}."

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
        for dsl_row in dsl_lines:
            row = []
            dsl_cells = dsl_row.split("|")
            dsl_cells = [c for c in dsl_cells if c]
            row.extend(tile_type_dict[dsl_cell] for dsl_cell in dsl_cells)
            print("".join(row))
        print(f'You are here: ({loc_x},{loc_y})')


    def parse_available_directions(self):
        if parser.tile_at(self.room.x, self.room.y - 1):
            response += "... north"
        elif parser.tile_at(self.room.x, self.room.y + 1):
            response += "... south"
        elif parser.tile_at(self.room.x + 1, self.room.y):
            response += "... east"
        elif parser.tile_at(self.room.x - 1, self.room.y):
            response += "... west"
        else:
            return
