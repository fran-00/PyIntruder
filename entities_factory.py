from entities import Entity, Item, Weapon, Curse, Consumable, ManaRechargers, Armor, NonPlayableCharacter, Enemy
import random


class EntityFactory:
    def __init__(self):
        pass
    

class EnemiesFactory(EntityFactory):
    def __init__(self):
        super().__init__()
        

Weapon(
    "Gelatinous Cube",
    "description",
    20,
    10
)