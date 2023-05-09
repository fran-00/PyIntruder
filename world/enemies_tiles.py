import random

from .map_tile import MapTile
from entities.factory import Factory


class EnemyTile_1(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        self.water = False
        super().__init__(x, y)
        self.enemy_list = [Factory().gel_cube, Factory().squirrel, Factory().helicopter]
        self.enemy = random.choice(self.enemy_list)


class EnemyTile_2(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        super().__init__(x, y)
        self.enemy_list = [Factory().hunter, Factory().hunter, Factory().eyes]
        self.enemy = random.choice(self.enemy_list)


class EnemyTile_3(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        super().__init__(x, y)
        self.enemy_list = [Factory().ants, Factory().trog, Factory().uncanny]
        self.enemy = random.choice(self.enemy_list)


class EnemyTile_4(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        super().__init__(x, y)
        self.enemy_list = [Factory().gnome]
        self.enemy = random.choice(self.enemy_list)


class EnemyTile_5(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        super().__init__(x, y)
        self.enemy_list = [Factory().ostoyae]
        self.enemy = random.choice(self.enemy_list)
