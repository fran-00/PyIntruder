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
        return f"{self.name} - {self.damage} DMG"


class Curse(Item):

    def __init__(self, name, description, level, value, damage, mana_cost):
        super().__init__(name, description, level, value)
        self.damage = damage
        self.mana_cost = mana_cost

    def __str__(self):
        return f"{self.name} - {self.damage} DMG"


class Healer(Item):

    def __init__(self, name, description, level, value, heal):
        super().__init__(name, description, level, value)
        self.heal = heal

    def __str__(self):
        return f"{self.name} - {self.heal} HP"


class ManaRecharger(Item):

    def __init__(self, name, description, level, value, mr):
        super().__init__(name, description, level, value)
        self.mr = mr
 
    def __str__(self):
        return f"{self.name} - {self.mr} MR"


class Armor(Item):

    def __init__(self, name, description, level, value, defence):
        super().__init__(name, description, level, value)
        self.defence = defence

    def __str__(self):
        return f"{self.name} - {self.defence} DEF"


class NonPlayableCharacter(Entity):

    def __init__(self, name, description, level, gold, inventory, hello, trade):
        super().__init__(name, description, level)
        self.gold = gold
        self.inventory = inventory
        self.hello = hello
        self.trade = trade
        self.sort_inventory()

    def sort_inventory(self):
        self.inventory.sort(key=lambda x: (x.__class__.__name__, x.name))
        return


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
