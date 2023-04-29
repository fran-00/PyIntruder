class Entity:

    def __init__(self, name, description, level):
        self.name = name
        self.description = description
        self.level = level

    def __str__(self):
        return self.name


class Item(Entity):

    def __init__(self, name, description, level, value):
        super().__init__(name, description, level)
        self.value = value
        self.value_if_sold = self.value // 10


class Weapon(Item):

    def __init__(self, name, description, level, value, damage):
        super().__init__(name, description, level, value)
        self.damage = damage

    def __str__(self):
        return self.name, self.damage


class Curse(Item):

    def __init__(self, name, description, level, value, damage, mana_cost):
        super().__init__(name, description, level, value)
        self.damage = damage
        self.mana_cost = mana_cost

    def __str__(self):
        return self.name, self.damage


class Healer(Item):

    def __init__(self, name, description, level, value, heal):
        super().__init__(name, description, level, value)
        self.heal = heal


class ManaRecharger(Item):

    def __init__(self, name, description, level, value, mr):
        super().__init__(name, description, level, value)
        self.mr = mr


class Armor(Item):

    def __init__(self, name, description, level, value, defence):
        super().__init__(name, description, level, value)
        self.defence = defence


class NonPlayableCharacter(Entity):

    def __init__(self, name, description, level, gold, items, hello, trade):
        super().__init__(name, description, level)
        self.gold = gold
        self.items = items
        self.inventory = self.sort_inventory(self.items)
        self.hello = hello
        self.trade = trade

    def sort_inventory(self, items):
        inventory = []
        for category in [Weapon, Curse, Healer, Armor]:
            inventory.extend(sorted([item for item in items if isinstance(
                item, category)], key=lambda item: item.name.lower()))
        return inventory


class Enemy(Entity):

    def __init__(self, name, description, level, hp, damage, alive):
        super().__init__(name, description, level)
        self.hp = hp
        self.damage = damage
        self.alive = alive

    def __str__(self):
        return self.name, self.hp

    def is_alive(self):
        return self.hp > 0
