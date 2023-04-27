import random


# >>>>> *** MANA RECHARGERS ***
class ManaRechargers:
    def __init__(self):
        raise NotImplementedError("Create a subclass instead!")

    def __str__(self):
        return f"{self.name} (+{self.mr} Mana)"

# >>>>> *** MANA RECHARGERS *** probabilmente conviene costruire una classe separata
class Ginseng(ManaRechargers):
    def __init__(self):
        self.name = "ginseng coffee"
        self.description = "Sweet and dense."
        self.damage = None
        self.defence = None
        self.heal = None
        self.mr = 50
        self.value = random.randint(200, 250)
        self.if_sold = self.value // 10
        self.weight = 0

class Campari(ManaRechargers):
    def __init__(self):
        self.name = "Campari Soda"
        self.description = "Red passion."
        self.damage = None
        self.defence = None
        self.heal = None
        self.mr = 60
        self.value = random.randint(250, 300)
        self.if_sold = self.value // 10
        self.weight = 0

class MinorFernPotion(ManaRechargers):
    def __init__(self):
        self.name = "minor Fern potion"
        self.description = "Please, consume in moderation. "
        self.damage = None
        self.defence = None
        self.heal = None
        self.mr = 70
        self.value = random.randint(300, 350)
        self.if_sold = self.value // 10
        self.weight = 0

class Album(ManaRechargers):
    def __init__(self):
        self.name = "Lift Your Skinny Fists Like Antennas to Heaven"
        self.description = "By Godspeed You! Black Emperor."
        self.damage = None
        self.defence = None
        self.heal = None
        self.mr = 80
        self.value = random.randint(350, 400)
        self.if_sold = self.value // 10
        self.weight = 0

class Grog(ManaRechargers):
    def __init__(self):
        self.name = "grog"
        self.description = " "
        self.damage = None
        self.defence = None
        self.heal = None
        self.mr = 90
        self.value =  random.randint(400, 450)
        self.if_sold = self.value // 10
        self.weight = 0

class MajorFernPotion(ManaRechargers):
    def __init__(self):
        self.name = "major Fern potion"
        self.description = "Seriously, this stuff is tough. Please consume in moderation. "
        self.damage = None
        self.defence = None
        self.heal = None
        self.mr = 100
        self.value =  random.randint(450, 500)
        self.if_sold = self.value // 10
        self.weight = 0




# >>>>> *** ARMOR ***
class Armor:
    def __init__(self):
        raise NotImplementedError("Do not create raw Armor objects")

    def __str__(self):
        return f"{self.name} ({self.defence} DEF)"

class RinaArmor(Armor):
    def __init__(self):
        self.name = "leaves armor"
        self.description = "This armor is made of white sheets and solid pieces of broom. It's not very protective but it's better than naked indeed."
        self.damage = None
        self.defence = random.randint(1, 2)
        self.heal = None
        self.mr = None
        self.value = random.randint(5000, 6000)
        self.if_sold = self.value // 10
        self.weight = 0

class FungineArmor(Armor):
    def __init__(self):
        self.name = "mushroom armor"
        self.description = "This armor is made of mushrooms."
        self.damage = None
        self.defence = random.randint(3, 4)
        self.heal = None
        self.mr = None
        self.value = random.randint(6000, 7000)
        self.if_sold = self.value // 10
        self.weight = 0

class ChairArmor(Armor):
    def __init__(self):
        self.name = "chair armor"
        self.description = "This armor is made of chairs."
        self.damage = None
        self.defence = random.randint(5, 6)
        self.heal = None
        self.mr = None
        self.value = random.randint(7000, 8000)
        self.if_sold = self.value // 10
        self.weight = 0

class IronArmor(Armor):
    def __init__(self):
        self.name = "iron armor"
        self.description = "This armor is made of iron."
        self.damage = None
        self.defence = random.randint(7, 8)
        self.heal = None
        self.mr = None
        self.value = random.randint(8000, 9000)
        self.if_sold = self.value // 10
        self.weight = 0

class TeslaArmor(Armor):
    def __init__(self):
        self.name = "Elon Musk Armor"
        self.description = "This armor is made of carbon nanotubules."
        self.damage = None
        self.defence = random.randint(9,10)
        self.heal = None
        self.mr = None
        self.value = random.randint(10000, 11000)
        self.if_sold = self.value // 10
        self.weight = 0

class MultidimensionalArmor(Armor):
    def __init__(self):
        self.name = "Multidimensional Armor"
        self.description = "This armor is made of carbon nanotubules."
        self.damage = None
        self.defence = random.randint(11,12)
        self.heal = None
        self.mr = None
        self.value = random.randint(11000, 12000)
        self.if_sold = self.value // 10
        self.weight = 0


# >>>>> *** MISSION ITEMS ***
class MissionItem:
    def __init__(self):
        raise NotImplementedError("Do not create raw MissionItem objects.")

    def __str__(self):
        return f"{self.name} "

class Specimen(MissionItem):
    def __init__(self):
        self.name = "specimen"
        self.description = "It's a specimen of the Perfect Fern. It is vivid green and moves slightly in the wind "
        self.damage = None
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = 0
        self.weight = 0
        
class Bottle(MissionItem):          # fai in modo che si possa riempire
    def __init__(self):
        self.name = "Thermo bottle"
        self.description = "Is an antique pink thermo bottle with botanical motifs drawn on it. Contains half a liter of water, and keeps it cold or hot for 12 hours. It also has a small cylindrical mesh container for making herbal teas."
        self.damage = None
        self.defence = None
        self.heal = 30
        self.value = 0
        self.weight = 0


# da qui in poi non sono sul dizionario
class Lights(MissionItem):
    def __init__(self):
        self.name = "lights of the nativity scene"
        self.description = "They're not supposed to be here: it's August 15th."

class Vents(MissionItem):
    def __init__(self):
        self.name = "water vents"
        self.description = "They're not supposed to be here: it's a forest!"
        
class Toupee(MissionItem):
    def __init__(self):
        self.name = "Enzo Paolo's toupee"
        self.description = "It's soft, fluffly and blonde."
        
class Knife(MissionItem):
    def __init__(self):
        self.name = "utility knife"
        self.description = "It's a cheap knife but full of tools, very useful. A very special person gave it to you."

class Phone(MissionItem):
    def __init__(self):
        self.name = "Priamo's Phone"
        self.description = "It contain a guide licence and an ID."

class Ropes(MissionItem):
    def __init__(self):
        self.name = "hemp ropes"
        self.description = "They're the strongest rope you could imagine."
        self.value = 9

class Fish(MissionItem):
    def __init__(self):
        self.name = "spiral fish carrier"
        self.description = "?"
        self.value = 8

class Dish(MissionItem):
    def __init__(self):
        self.name = "shoe rack dish drainer"
        self.description = "?"
        self.value = 7

class Holder(MissionItem):
    def __init__(self):
        self.name = "towel holder made of flesh"
        self.description = "It's an arm."
        self.value = 7

