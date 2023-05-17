from entities.factory import EntitiesFactory as entities
from world.map_tile import MapTile


class StartTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Clearing'
        super().__init__(x, y)
        self.environment = [entities().car, entities().table]


class LittleoTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Little(o) Shop'
        super().__init__(x, y)
        self.talker = entities().littleo


class BlacksmithTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Blacksmith'
        super().__init__(x, y)
        self.talker = entities().blacksmith


class ChestTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Chest'
        super().__init__(x, y)


class FernsTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Ferns'
        super().__init__(x, y)
        self.talker = entities().ferns


class FountainTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Fountain'
        super().__init__(x, y)
        self.water = True


class IntruderTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Intruder'
        super().__init__(x, y)
        self.talker = entities().intruder


class RiverTile(MapTile):
    def __init__(self, x, y):
        self.name = 'River'
        super().__init__(x, y)


class OakTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Oak'
        super().__init__(x, y)
        self.talker = entities().oak


class PathTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        super().__init__(x, y)


class TempleTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Temple'
        super().__init__(x, y)
        self.talker = entities().monk


class VictoryTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Victory'
        super().__init__(x, y)
