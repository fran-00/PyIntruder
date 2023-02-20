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
        super().__init__(name, description, level, value, damage)
        self.damage = damage
        
    def __str__(self):
        return self.name, self.damage


class Curse(Item):
    
    def __init__(self, name, description, level, value, damage, mana_cost):
        super().__init__(name, description, level, value, damage)
        self.damage = damage
        self.mana_cost = mana_cost
    
    def __str__(self):
        return self.name, self.damage


class Consumable(Item):
    
    def __init__(self, name, description, level, value, heal):
        super().__init__(name, description, level, value)
        self.heal = heal


class ManaRecharger(Item):
    
    def __init__(self, name, description, value, mr):
        super().__init__(name, description, value)
        self.mr = mr


class Armor(Item):
    
    def __init__(self, name, description, value, defence):
        super().__init__(name, description, value)
        self.defence = defence


class NonPlayableCharacter(Entity):
    
    def __init__(self, name, description, gold, inventory):
        super().__init__(name, description)
        self.gold = gold
        self.inventory = inventory


class Enemy(Entity):

    def __init__(self, name, description, hp, damage):
        super().__init__(name, description)
        self.hp = hp
        self.damage = damage

    def __str__(self):
        return self.name, self.hp

    def is_alive(self):
        return self.hp > 0

        # import intro_alive, intro_dead, talk_alive_talk_dead
        # from a .json