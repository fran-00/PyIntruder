

class Entity:
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
        
        # importa la description da un json
    
    def __str__(self):
        return self.name


class Item(Entity):
    
    def __init__(self, name, description, value):
        super().__init__(name, description)
        self.value = value
        self.value_if_sold = self.value // 10


class Weapon(Item):
    
    def __init__(self, name, description, value, damage):
        super().__init__(name, description, value, damage)
        self.damage = damage


class Curse(Item):
    
    def __init__(self, name, description, value, damage, mana_cost):
        super().__init__(name, description, value, damage)
        self.damage = damage
        self.mana_cost = mana_cost


class Consumable(Item):
    
    def __init__(self, name, description, value, heal):
        super().__init__(name, description, value)
        self.heal = heal


class ManaRechargers(Item):
    
    def __init__(self, name, description, value, mr):
        super().__init__(name, description, value)
        self.mr = mr
     
   
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