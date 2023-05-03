import json


with open('entities/data/items_data.json') as f:
    items_data = json.load(f)


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
        self.damage = damage

    def __str__(self):
        return f"{self.name} - {self.damage} DMG"


class Curse(Item):

    def __init__(self, name, level, value, damage, mana_cost):
        super().__init__(name, level, value)
        self.damage = damage
        self.mana_cost = mana_cost

    def __str__(self):
        return f"{self.name} - {self.damage} DMG - {self.mana_cost} Mana"


class Healer(Item):

    def __init__(self, name, level, value, heal):
        super().__init__(name, level, value)
        self.heal = heal

    def __str__(self):
        return f"{self.name} - {self.heal} HP"


class ManaRecharger(Item):

    def __init__(self, name, level, value, mr):
        super().__init__(name, level, value)
        self.mr = mr
 
    def __str__(self):
        return f"{self.name} - {self.mr} MR"


class Armor(Item):

    def __init__(self, name, level, value, defence):
        super().__init__(name, level, value)
        self.defence = defence

    def __str__(self):
        return f"{self.name} - {self.defence} DEF"


class NonPlayableCharacter(Entity):

    def __init__(self, name, level, gold, inventory, hello, trade):
        super().__init__(name, level)
        self.gold = gold
        self.inventory = inventory
        self.hello = hello
        self.trade = trade
        self.sort_inventory()

    def sort_inventory(self):
        self.inventory.sort(key=lambda x: (x.__class__.__name__, x.name))
        return


class Enemy(Entity):

    def __init__(self, name, level, hp, damage):
        super().__init__(name, level)
        self.hp = hp
        self.damage = damage

    def __str__(self):
        return self.name, self.hp

    def is_alive(self):
        return self.hp > 0
