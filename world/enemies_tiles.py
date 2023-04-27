import random

from .map_tile import MapTile
import old_entities_data.enemies as e


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
        
        self.enemy_list = [e.GelCube(), e.Squirrel(), e.Helicopter()]
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
        
        self.enemy_list = [e.Cops(), e.MushroomHunter()]
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
        
        self.enemy_list = [e.Bug(), e.Eyes(), e.Ants(), e.Trog()]
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

        self.enemy_list = [e.UncannyValley(), e.Paranoia(), e.Gnome()]
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

        self.enemy_list = [e.Herobrine(), e.RubberJohnny(), e.ArmillariaOstoyae()]
        self.enemy = random.choice(self.enemy_list)
        super().__init__(x, y)

