import random

from .map_tile import MapTile
from entities.factories import enemies as e


class EnemyTile_1(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        self.water = False
        super().__init__(x, y)
        self.enemy_list = [e().gel_cube, e().squirrel, e().helicopter]
        self.enemy = random.choice(self.enemy_list)


class EnemyTile_2(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        super().__init__(x, y)
        self.enemy_list = [e().hunter, e().hunter, e().eyes]
        self.enemy = random.choice(self.enemy_list)


class EnemyTile_3(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        super().__init__(x, y)
        self.enemy_list = [e().ants, e().trog, e().uncanny]
        self.enemy = random.choice(self.enemy_list)


class EnemyTile_4(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        super().__init__(x, y)
        self.enemy_list = [e().gnome]
        self.enemy = random.choice(self.enemy_list)


class EnemyTile_5(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        super().__init__(x, y)
        self.enemy_list = [e().ostoyae]
        self.enemy = random.choice(self.enemy_list)
