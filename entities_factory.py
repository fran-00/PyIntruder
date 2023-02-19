from entities import Entity, Item, Weapon, Curse, Consumable, ManaRechargers, Armor, NonPlayableCharacter, Enemy
import random


class EntityFactory:
    def __init__(self):
        pass
    

class EnemiesFactory(EntityFactory):
    def __init__(self):
        super().__init__()
        

ats = Consumable(
    "ATS",
    "A liquid which is almost, but not quite, entirely unlike tea.",
    random.randint(310, 340),
    70
)