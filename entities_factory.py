from entities import Entity, Item, Weapon, Enemy, Curse, Consumable, ManaRechargers, Armor, NonPlayableCharacter
import random, json
  

with open('items_data.json') as f:
    items_data = json.load(f)

with open('enemies_data.json') as ef:
    enemies_data = json.load(ef)


class ItemsFactory:
    def __init__(self):
        self.ats = Consumable(
            "ATS",
            items_data["consumables"]["Advanced Tea Substitute"],
            random.randint(310, 340),
            70
        )


class EnemiesFactory:
    
    def __init__(self):
        self.gel_cube = Enemy(
            "Gelatinous Cube",
            items_data["gel cube"]["intro_alive"],
            20,
            10
        )
        

print(ItemsFactory().ats.description)
print(EnemiesFactory.gel_cube.description)


