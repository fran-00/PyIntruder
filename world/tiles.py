import random

from entities.factories.npcs_factory import NPCsFactory as NPCf
from entities.factories.weapons_factory import WeaponsFactory as Wf
from entities.factories.armors_factory import ArmorsFactory as Af
from entities.factories.healers_factory import HealersFactory as Hf
from entities.factories.quest_items_factory import QuestItemsFatory as QIf
from entities.factories.enemies_factory import EnemiesFactory as Ef
from world.map_tile import MapTile


class StartTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Clearing'
        self.description = "You are in a clearing. You arrived with your car from the west and the road ends in the east, where a path that climbs the mountain begins. A dense network of trees prevents the passage in any other direction. Your car is parked on the north side of the clearing, there is no one else parked."
        self.inventory = []
        self.talker = None
        self.enemy = None
        super().__init__(x, y)


class Little_oTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Little(o) Shop'
        self.description = "They say it is only infinitesimally probable to be here."
        self.inventory = []
        self.talker = NPCf().littleo
        self.enemy = None
        super().__init__(x, y)


class BlacksmithTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Blacksmith'
        self.description = "You are in a blacksmith's shop. He is working on an anvil by striking a hot iron with a hammer. The room is small, full of tools, and it's hot as hell."
        self.inventory = []
        self.talker = NPCf().blacksmith
        self.enemy = None
        super().__init__(x, y)


class ChestTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Chest'
        self.description = "There's a chest here.\n"
        self.inventory = []
        self.talker = None
        self.enemy = None
        super().__init__(x, y)


class FernsTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Ferns'
        self.description = "A lot of ferns."
        self.inventory = []
        self.talker = NPCf().ferns
        self.enemy = None
        super().__init__(x, y)


class IntruderTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Intruder'
        self.description = "It shouldn't be here"
        self.inventory = []
        self.talker = NPCf.intruder()
        self.enemy = None
        super().__init__(x, y)


class OakTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Oak'
        self.description = "There's n Oak here."
        self.inventory = []
        self.talker = NPCf().oak
        self.enemy = None
        super().__init__(x, y)


class PathTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        self.description = "The path is a boring place to stop: usually you just walk over it to go somewhere (wherever it is). This path in particular is uphill and surrounded by tall, green trees. Noises can be heard coming from the trees, maybe you're not alone..."
        self.inventory = []
        self.talker = None
        self.enemy = None
        super().__init__(x, y)


class TempleTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Temple'
        self.description = "You are in a temple. Strange symbols made up of concentric circles adorn the walls. A monk prays in front of an altar filled with a liquid of a strange color."
        self.inventory = []
        self.talker = NPCf().monk
        self.enemy = None
        super().__init__(x, y)


class VictoryTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Victory'
        self.description = None
        self.inventory = []
        self.talker = None
        self.enemy = None
        super().__init__(x, y)
