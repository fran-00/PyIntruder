from entities import Entity, Item, Weapon, Enemy, Curse, Consumable, ManaRecharger, Armor, NonPlayableCharacter
import random, json
  

with open('items_data.json') as f:
    items_data = json.load(f)

with open('enemies_data.json') as ef:
    enemies_data = json.load(ef)

with open('npcs_data.json') as nf:
    npcs_data = json.load(nf)


class ItemsFactory:
    
    def __init__(self):
        self.ats = Consumable(
            "Advanced Tea Substitute",
            items_data["consumables"]["ats"],
            1,
            random.randint(310, 340),
            70
        )


class EnemiesFactory:
    
    def __init__(self):
        self.gel_cube = Enemy(
            "Gelatinous Cube",
            enemies_data["gel cube"]["intro_alive"],
            1,
            20,
            10
        )


class NPCsFactory:
    
    def __init__(self):
        self.littleo = NonPlayableCharacter(
            "Little(o)",
            npcs_data["littleo"]["description"],
            None,
            1000,
            [ItemsFactory().ats]
        )


class WeaponFactory:
    
    def __init__(self):
        self.wireless_wire = Weapon(
            "Wireless Wire",
            items_data["weapons"]["wireless wire"],
            1,
            15,
            20,
        )



print(ItemsFactory().ats.description)
print(EnemiesFactory().gel_cube.level)
print(NPCsFactory().littleo.description)
print(WeaponFactory().wireless_wire.description)

