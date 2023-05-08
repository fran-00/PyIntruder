from entities.factories import npcs, surroundings
from world.map_tile import MapTile


class StartTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Clearing'
        super().__init__(x, y)
        self.environment = [surroundings().car]


class LittleoTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Little(o) Shop'
        super().__init__(x, y)
        self.talker = npcs().littleo


class BlacksmithTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Blacksmith'
        super().__init__(x, y)
        self.talker = npcs().blacksmith


class ChestTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Chest'
        super().__init__(x, y)


class FernsTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Ferns'
        super().__init__(x, y)
        self.talker = npcs().ferns


class IntruderTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Intruder'
        super().__init__(x, y)
        self.talker = npcs().intruder


class OakTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Oak'
        super().__init__(x, y)
        self.talker = npcs().oak


class PathTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        super().__init__(x, y)


class TempleTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Temple'
        super().__init__(x, y)
        self.talker = npcs().monk


class VictoryTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Victory'
        super().__init__(x, y)
