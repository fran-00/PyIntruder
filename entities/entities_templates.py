import json, random


with open('entities/data/items_data.json') as f:
    items_data = json.load(f)

with open('entities/data/npcs_data.json') as nf:
    npcs_data = json.load(nf)

with open('entities/data/enemies_data.json') as ef:
    enemies_data = json.load(ef)


class Entity:

    def __init__(self, name, level):
        self.name = name
        self.level = level

    def __str__(self):
        return self.name


class Item(Entity):

    def __init__(self, name, level, value):
        super().__init__(name, level)
        self.value = value
        self.value_if_sold = self.value // 10


class Weapon(Item):

    def __init__(self, name, level, value, damage):
        super().__init__(name, level, value)
        self.description = items_data["weapons"][f"{self.name}".lower()]
        self.damage = damage

    def __str__(self):
        return f"{self.name} - {self.damage} DMG"


class Curse(Item):

    def __init__(self, name, level, value, damage, mana_cost):
        super().__init__(name, level, value)
        self.description = items_data["curses"][f"{self.name}".lower()]
        self.damage = damage
        self.mana_cost = mana_cost

    def __str__(self):
        return f"{self.name} - {self.damage} DMG - {self.mana_cost} Mana"


class Healer(Item):

    def __init__(self, name, level, value, heal):
        super().__init__(name, level, value)
        self.description = items_data["healers"][f"{self.name}".lower()]
        self.heal = heal

    def __str__(self):
        return f"{self.name} - {self.heal} HP"


class ManaRecharger(Item):

    def __init__(self, name, level, value, mr):
        super().__init__(name, level, value)
        self.description = items_data["mana rechargers"][f"{self.name}".lower()]
        self.mr = mr
 
    def __str__(self):
        return f"{self.name} - {self.mr} MR"


class Armor(Item):

    def __init__(self, name, level, value, defence):
        super().__init__(name, level, value)
        self.description = items_data["armors"][f"{self.name}".lower()]
        self.defence = defence

    def __str__(self):
        return f"{self.name} - {self.defence} DEF"


class NonPlayableCharacter(Entity):

    def __init__(self, name, level, gold, inventory, trade):
        super().__init__(name, level)
        self.description = npcs_data[f"{self.name}".lower()]["description"]
        self.gold = gold
        self.inventory = inventory
        self.trade = trade
        self.sort_inventory()

    def sort_inventory(self):
        self.inventory.sort(key=lambda x: (x.__class__.__name__, x.name))
        return

    def get_random_dialogue(self, npc_name=str):
        # FIXME:
        dialogues = npcs_data[npc_name]['dialogues']
        dialogue = random.choice(list(dialogues.values()))
        return dialogue


class Enemy(Entity):

    def __init__(self, name, level, hp, damage):
        super().__init__(name, level)
        self.description = enemies_data[f"{self.name}".lower()]["intro_alive"]
        self.hp = hp
        self.damage = damage

    def __str__(self):
        return self.name, self.hp

    def is_alive(self):
        return self.hp > 0
