import random

from .map_tile import MapTile
import old_entities_data.enemies as e


# >>>> FIGHT
# |X1|
class EnemyTile_1(MapTile):
    def __init__(self, x, y):
        self.name = 'ET1'
        self.talker = None
        self.enemy = None
        self.description = 'You are on a path surrounded by trees.'
        self.examine = None
        self.seen = False
        self.env_obj = []
        self.water = False
        r = random.randint(1, 4)
        if r == 1:
            self.enemy = enemies.GelCube()
        elif r == 2:
            self.enemy = enemies.NoMask()
        elif r == 3:
            self.enemy = enemies.Squirrel()
        else:
            self.enemy = enemies.Helicopter()
        super().__init__(x, y)


# |X2|
class EnemyTile_2(MapTile):
    def __init__(self, x, y):
        self.name = 'ET2'
        self.talker = None
        self.enemy = None
        self.description = 'You are on a path surrounded by trees.'
        self.examine = None
        self.seen = False
        self.env_obj = []
        self.water = False
        r = random.randint(1, 4)
        if r == 1:
            self.enemy = enemies.Cops()
        elif r == 2:
            self.enemy = enemies.MushroomHunter()
        elif r == 3:
            self.enemy = enemies.Incel()
        else:
            self.enemy = enemies.JacobChansley()
        super().__init__(x, y)


# |X3|
class EnemyTile_3(MapTile):
    def __init__(self, x, y):
        self.name = 'ET3'
        self.talker = None
        self.enemy = None
        self.description = 'You are on a path surrounded by trees.'
        self.examine = None
        self.seen = False
        self.env_obj = []
        self.water = False
        r = random.randint(1, 4)
        if r == 1:
            self.enemy = enemies.Bug()
        elif r == 2:
            self.enemy = enemies.Eyes()
        elif r == 3:
            self.enemy = enemies.Ants()
        else:
            self.enemy = enemies.Trog()
        super().__init__(x, y)


# |X4|
class EnemyTile_4(MapTile):
    def __init__(self, x, y):
        self.name = 'ET4'
        self.talker = None
        self.enemy = None
        self.description = 'You are on a path surrounded by trees.'
        self.examine = None
        self.seen = False
        self.env_obj = []
        self.water = False
        r = random.randint(1, 4)
        if r == 1:
            self.enemy = enemies.UncannyValley()
        elif r == 2:
            self.enemy = enemies.Paranoia()
        elif r == 3:
            self.enemy = enemies.Gnome()
        else:
            self.enemy = enemies.Mcu()
        super().__init__(x, y)


# |X5|
class EnemyTile_5(MapTile):
    def __init__(self, x, y):
        self.name = 'ET5'
        self.talker = None
        self.enemy = None
        self.description = 'You are on a path surrounded by trees.'
        self.examine = None
        self.seen = False
        self.env_obj = []
        self.water = False
        r = random.randint(1, 4)
        if r == 1:
            self.enemy = enemies.Herobrine()
        elif r == 2:
            self.enemy = enemies.RubberJohnny()
        elif r == 3:
            self.enemy = enemies.ArmillariaOstoyae()
        else:
            self.enemy = enemies.MetaVerse()
        super().__init__(x, y)

