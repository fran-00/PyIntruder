from entities import Entity, Item, Weapon, Curse, Consumable, ManaRechargers, Armor, NonPlayableCharacter, Enemy
import random, json
  

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


class EnemiesFactory():
    def __init__(self):
        pass
        

print(ItemsFactory().ats.description)

