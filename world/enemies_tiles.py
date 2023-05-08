import random

from .map_tile import MapTile
from entities.factories import enemies as e


class EnemyTile_1(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        self.talker = None
        self.examine = None
        self.seen = False
        self.env_obj = []
        self.water = False
        self.enemy_list = [Ef().gel_cube, Ef().squirrel, Ef().helicopter]
        self.enemy = random.choice(self.enemy_list)
        super().__init__(x, y)


class EnemyTile_2(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        self.talker = None
        self.examine = None
        self.seen = False
        self.env_obj = []
        self.enemy_list = [Ef().hunter, Ef().hunter, Ef().eyes]
        self.enemy = random.choice(self.enemy_list)
        super().__init__(x, y)


class EnemyTile_3(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        self.talker = None
        self.examine = None
        self.seen = False
        self.env_obj = []
        self.enemy_list = [Ef().ants, Ef().trog, Ef().uncanny]
        self.enemy = random.choice(self.enemy_list)
        super().__init__(x, y)


class EnemyTile_4(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        self.talker = None
        self.examine = None
        self.seen = False
        self.env_obj = []
        self.enemy_list = [Ef().gnome]
        self.enemy = random.choice(self.enemy_list)
        super().__init__(x, y)


class EnemyTile_5(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        self.talker = None
        self.examine = None
        self.seen = False
        self.env_obj = []
        self.enemy_list = [Ef().ostoyae]
        self.enemy = random.choice(self.enemy_list)
        super().__init__(x, y)

