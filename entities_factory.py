import entities
import random


class EntityFactory:
    def __init__(self):
        pass
    

class EnemiesFactory(EntityFactory):
    def __init__(self):
        super().__init__()
        

entities.Weapon(
    "Gelatinous Cube",
    "description",
    20,
    10
)