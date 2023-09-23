import random

from .templates import Entity
from .factory import ItemsFactory as items

from world.parser import WorldCreator
import world.tiles as world
from engine.utils.combat_system import Combat
from gui.styles.decorators import *


class Player(Entity):
    def __init__(self):
        self.name = 'Your Name Here'
        self.x = WorldCreator.start_tile_location[0]
        self.y = WorldCreator.start_tile_location[1]
        self.room = WorldCreator.tile_at(self.x, self.y)

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
    
    def update_player_room(self):
        self.room = WorldCreator.tile_at(self.x, self.y)
        return

    def get_player_data(self):
        return list(self.__dict__.values())

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
        d20 = random.randint(1, 20)
        if d20 == 20:
            self.room.enemy.alive = False
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
        return (
            f"<b>Level</b> : {self.lvl}<br>"
            f"<b>HP</b> : {self.hp}/{self.max_hp}<br>"
            f"<b>Mana</b> : {self.mana}/{self.max_mana}<br>"
            f"<b>§</b> : {self.gold}<br>"
            f"<b>XP</b> : {self.xp}/{self.xp_modifier}<br>"
            f"<b>Weapon equipped</b> : {self.current_weapon}<br>"
            f"<b>Turn</b> : {self.turn}<br>"
            f"<b>Location</b> : {self.x}.{self.y} - {self.room.name}"
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
        dsl_lines = WorldCreator.world_dsl.splitlines()
        dsl_lines = [x for x in dsl_lines if x]
        for dsl_row in dsl_lines:
            row = []
            dsl_cells = dsl_row.split("|")
            dsl_cells = [c for c in dsl_cells if c]
            row.extend(tile_type_dict[dsl_cell] for dsl_cell in dsl_cells)
            print("".join(row))
        print(f'You are here: ({loc_x},{loc_y})')


    def parse_available_directions(self):
        if WorldCreator.tile_at(self.room.x, self.room.y - 1):
            response += "... north"
        elif WorldCreator.tile_at(self.room.x, self.room.y + 1):
            response += "... south"
        elif WorldCreator.tile_at(self.room.x + 1, self.room.y):
            response += "... east"
        elif WorldCreator.tile_at(self.room.x - 1, self.room.y):
            response += "... west"
        else:
            return
