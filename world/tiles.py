import random

from entities.factories.npcs_factory import NPCsFactory as NPCf
from world.map_tile import MapTile


class StartTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Clearing'
        self.inventory = []
        self.talker = None
        self.enemy = None
        super().__init__(x, y)


class LittleoTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Little(o) Shop'
        self.inventory = []
        self.talker = NPCf().littleo
        self.enemy = None
        super().__init__(x, y)


class BlacksmithTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Blacksmith'
        self.inventory = []
        self.talker = NPCf().blacksmith
        self.enemy = None
        super().__init__(x, y)


class ChestTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Chest'
        self.inventory = []
        self.talker = None
        self.enemy = None
        super().__init__(x, y)


class FernsTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Ferns'
        self.inventory = []
        self.talker = NPCf().ferns
        self.enemy = None
        super().__init__(x, y)


class IntruderTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Intruder'
        self.inventory = []
        self.talker = NPCf.intruder()
        self.enemy = None
        super().__init__(x, y)


class OakTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Oak'
        self.inventory = []
        self.talker = NPCf().oak
        self.enemy = None
        super().__init__(x, y)


class PathTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        self.inventory = []
        self.talker = None
        self.enemy = None
        super().__init__(x, y)


class TempleTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Temple'
        self.inventory = []
        self.talker = NPCf().monk
        self.enemy = None
        super().__init__(x, y)


class VictoryTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Victory'
        self.inventory = []
        self.talker = None
        self.enemy = None
        super().__init__(x, y)
