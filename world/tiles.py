from entities.factories import npcs, surroundings
from world.map_tile import MapTile


class StartTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Clearing'
        self.inventory = []
        self.environment = [surroundings().chest]
        self.talker = None
        self.enemy = None
        super().__init__(x, y)


class LittleoTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Little(o) Shop'
        self.inventory = []
        self.environment = []
        self.talker = npcs().littleo
        self.enemy = None
        super().__init__(x, y)


class BlacksmithTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Blacksmith'
        self.inventory = []
        self.environment = []
        self.talker = npcs().blacksmith
        self.enemy = None
        super().__init__(x, y)


class ChestTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Chest'
        self.inventory = []
        self.environment = []
        self.talker = None
        self.enemy = None
        super().__init__(x, y)


class FernsTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Ferns'
        self.inventory = []
        self.environment = []
        self.talker = npcs().ferns
        self.enemy = None
        super().__init__(x, y)


class IntruderTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Intruder'
        self.inventory = []
        self.environment = []
        self.talker = npcs().intruder
        self.enemy = None
        super().__init__(x, y)


class OakTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Oak'
        self.inventory = []
        self.environment = []
        self.talker = npcs().oak
        self.enemy = None
        super().__init__(x, y)


class PathTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        self.inventory = []
        self.environment = []
        self.talker = None
        self.enemy = None
        super().__init__(x, y)


class TempleTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Temple'
        self.inventory = []
        self.environment = []
        self.talker = npcs().monk
        self.enemy = None
        super().__init__(x, y)


class VictoryTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Victory'
        self.inventory = []
        self.environment = []
        self.talker = None
        self.enemy = None
        super().__init__(x, y)
