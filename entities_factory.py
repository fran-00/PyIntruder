from entities import Entity, Item, Weapon, Curse, Consumable, ManaRechargers, Armor, NonPlayableCharacter, Enemy
import random, json


class EntityFactory:
    def __init__(self):
        pass
    

class EnemiesFactory(EntityFactory):
    def __init__(self):
        super().__init__()


with open('items_data.json') as f:
    items_data = json.load(f)


class ItemsFactory:
    def __init__(self):
        self.ats = Consumable(
            "ATS",
            items_data["consumables"]["Advanced Tea Substitute"],
            random.randint(310, 340),
            70
        )


print(ItemsFactory().ats.description)