import random

from .map_tile import MapTile
from entities.factory import EntitiesFactory as enemies


class EnemyTile_1(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        self.water = False
        super().__init__(x, y)
        self.enemy_list = [enemies().gel_cube, enemies().squirrel, enemies().helicopter]
        self.enemy = random.choice(self.enemy_list)


class EnemyTile_2(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        super().__init__(x, y)
        self.enemy_list = [enemies().hunter, enemies().hunter, enemies().eyes]
        self.enemy = random.choice(self.enemy_list)


class EnemyTile_3(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        super().__init__(x, y)
        self.enemy_list = [enemies().ants, enemies().trog, enemies().uncanny]
        self.enemy = random.choice(self.enemy_list)


class EnemyTile_4(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        super().__init__(x, y)
        self.enemy_list = [enemies().gnome]
        self.enemy = random.choice(self.enemy_list)


class EnemyTile_5(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        super().__init__(x, y)
        self.enemy_list = [enemies().ostoyae]
        self.enemy = random.choice(self.enemy_list)
