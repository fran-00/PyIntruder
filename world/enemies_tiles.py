import random

from .map_tile import MapTile
from entities.factories import enemies_factory as e


# >>>> FIGHT
# |X1|
class EnemyTile_1(MapTile):
    def __init__(self, x, y):
        self.name = 'ET1'
        self.talker = None
        self.description = 'You are on a path surrounded by trees.'
        self.examine = None
        self.seen = False
        self.env_obj = []
        self.water = False
        
        self.enemy_list = [e.Lv1().gel_cube, e.Lv1().squirrel, e.Lv1().helicopter]
        self.enemy = random.choice(self.enemy_list)
        super().__init__(x, y)


# |X2|
class EnemyTile_2(MapTile):
    def __init__(self, x, y):
        self.name = 'ET2'
        self.talker = None
        self.description = 'You are on a path surrounded by trees.'
        self.examine = None
        self.seen = False
        self.env_obj = []
        self.water = False
        
        self.enemy_list = [e.Lv2().hunter, e.Lv2().hunter, e.Lv2().eyes]
        self.enemy = random.choice(self.enemy_list)
        super().__init__(x, y)


# |X3|
class EnemyTile_3(MapTile):
    def __init__(self, x, y):
        self.name = 'ET3'
        self.talker = None
        self.description = 'You are on a path surrounded by trees.'
        self.examine = None
        self.seen = False
        self.env_obj = []
        self.water = False
        
        self.enemy_list = [e.Lv3().ants, e.Lv3().trog, e.Lv3().uncanny]
        self.enemy = random.choice(self.enemy_list)
        super().__init__(x, y)


# |X4|
class EnemyTile_4(MapTile):
    def __init__(self, x, y):
        self.name = 'ET4'
        self.talker = None
        self.description = 'You are on a path surrounded by trees.'
        self.examine = None
        self.seen = False
        self.env_obj = []
        self.water = False

        self.enemy_list = [e.Lv4().gnome]
        self.enemy = random.choice(self.enemy_list)
        super().__init__(x, y)


# |X5|
class EnemyTile_5(MapTile):
    def __init__(self, x, y):
        self.name = 'ET5'
        self.talker = None
        self.description = 'You are on a path surrounded by trees.'
        self.examine = None
        self.seen = False
        self.env_obj = []
        self.water = False

        self.enemy_list = [e.Lv5().ostoyae]
        self.enemy = random.choice(self.enemy_list)
        super().__init__(x, y)

