import json
import random


with open('entities/data/items_data.json') as f:
    items_data = json.load(f)

with open('entities/data/npcs_data.json') as nf:
    npcs_data = json.load(nf)

with open('entities/data/enemies_data.json') as ef:
    enemies_data = json.load(ef)


class Entity:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class NonPlayableCharacter(Entity):

    def __init__(self, name, inventory, trade):
        super().__init__(name)
        self.description = npcs_data[f"{self.name}".lower()]["description"]
        self.gold = 100000
        self.inventory = inventory
        self.trade = trade
        self.sort_inventory()

    def sort_inventory(self):
        self.inventory.sort(key=lambda x: (x.__class__.__name__, x.name))
        return

    def get_random_opening_sentence(self, npc_name=str):
        sentences = npcs_data[npc_name.lower()]['opening sentence']
        opening_sentence = random.choice(list(sentences.values()))
        return opening_sentence


class Enemy(Entity):

    def __init__(self, name, level, hp, damage):
        super().__init__(name)
        self.description_if_alive = enemies_data[f"{self.name}".lower()]["intro_alive"]
        self.description_if_dead = enemies_data[f"{self.name}".lower()]["intro_dead"]
        self.level = level
        self.hp = hp
        self.damage = damage

    def __str__(self):
        return self.name, self.hp

    def is_alive(self):
        return self.hp > 0


class Item(Entity):

    def __init__(self, name):
        super().__init__(name)
        self.value = 0
        self.collectable = True
        self.marketable = True
        self.openable = False

    def calculate_value(self, n):
        range_value = n * 0.3
        return round(random.uniform(n - range_value, n + range_value), 2)


class Weapon(Item):

    def __init__(self, name, damage):
        super().__init__(name)
        self.description = items_data["weapons"][f"{self.name}".lower()]
        self.damage = damage
        self.value = self.calculate_value(self.damage)

    def __str__(self):
        return f"{self.name} - {self.damage} DMG"


class Curse(Item):

    def __init__(self, name, damage):
        super().__init__(name)
        self.description = items_data["curses"][f"{self.name}".lower()]
        self.damage = damage
        self.mana_cost = self.damage * 4
        self.value = self.calculate_value(self.damage)

    def __str__(self):
        return f"{self.name} - {self.damage} DMG - {self.mana_cost} Mana"


class Healer(Item):

    def __init__(self, name, heal):
        super().__init__(name)
        self.description = items_data["healers"][f"{self.name}".lower()]
        self.heal = heal
        self.value = self.calculate_value(self.heal)

    def __str__(self):
        return f"{self.name} - {self.heal} HP"


class ManaRecharger(Item):

    def __init__(self, name, mr):
        super().__init__(name)
        self.description = items_data["mana rechargers"][f"{self.name}".lower()]
        self.mr = mr
        self.value = self.calculate_value(self.mr)

    def __str__(self):
        return f"{self.name} - {self.mr} MR"


class Armor(Item):

    def __init__(self, name, defence):
        super().__init__(name)
        self.description = items_data["armors"][f"{self.name}".lower()]
        self.defence = defence
        self.value = self.calculate_value(self.defence)

    def __str__(self):
        return f"{self.name} - {self.defence} DEF"


class Surrounding(Item):

    def __init__(self, name, inventory, openable=False):

        super().__init__(name)
        self.description = items_data["surroundings"][f"{self.name}".lower()]
        self.inventory = inventory
        self.collectable = False
        self.marketable = False
        self.openable = openable


class MissionRelatedItem(Item):

    def __init__(self, name, openable=False):

        super().__init__(name)
        self.description = items_data["mission related items"][f"{self.name}".lower()]
        self.marketable = False
        self.openable = openable
