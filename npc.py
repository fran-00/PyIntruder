import random

import items
import items_data

# NPC MODULE
class NonPlayableCharacter():
    def __init__(self):
        raise NotImplementedError("Do not create raw NPC objects. Create a subclass instead.")
    
    def __str__(self):
        return self.name


class Littleo(NonPlayableCharacter):       # only curses
    def __init__(self):
        self.name = "Little(o)"
        self.description = "Cool"
        self.gold = 10000
        self.inventory = random.sample(items_data.curses_list, 7)

class InnKeeper(NonPlayableCharacter):      # only consumables
    def __init__(self):
        self.name = "Innkeeper"
        self.description = "Fat and ugly."
        self.gold = 10000
        self.inventory = random.sample(items_data.consumables_list, 5)


class Blacksmith(NonPlayableCharacter):      # only weapons and armors
    def __init__(self):
        self.name = "Blacksmith"
        self.description = "Chad."
        self.gold = 10000
        self.inventory = random.sample(items_data.weapons_armors, 10)

class Merchant(NonPlayableCharacter):      # only mr
    def __init__(self):
        self.name = "Merchant"
        self.description = "Chad."
        self.gold = 10000
        self.inventory = random.sample(items_data.all_objects, 20)

class Monk(NonPlayableCharacter):      # only mr
    def __init__(self):
        self.name = "Monk"
        self.description = "Chad."
        self.gold = 10000
        self.inventory = random.sample(items_data.mrs_list, 5)          # FIXME random.choices (con le ripetizioni) non funziona, dice che int non è qualcosa

class Ferns(NonPlayableCharacter):
    def __init__(self):
        self.name = "Ferns"
        self.description = "Green and worried."
        self.inventory =  [items.Specimen()]

class RinaCasti(NonPlayableCharacter):
    def __init__(self):
        self.name = "Rina Casti"
        self.description = "> "
        self.gold = 1000
        self.inventory =  []


class Intruder(NonPlayableCharacter):
    def __init__(self):
        self.name = "Supreme Intruder"
        self.description = "You're not supposed to be here."
        self.inventory = [items.Manuport()]

class Oak(NonPlayableCharacter):
    def __init__(self):
        self.name = "Oak"
        self.description = "Wise."
        self.inventory = [items.Modification()]

class EnzoPaolo(NonPlayableCharacter):
    def __init__(self):
        self.name = "Enzo Paolo"
        self.description = "(Was)Blonde and sexy."
        self.inventory = [items.Modification()]

class Priamo(NonPlayableCharacter):
    def __init__(self):
        self.name = "Priamo Tolu"
        self.description = "He's Priamo."
        self.gold = 1000
        self.inventory =  [items.Manuport()]

class Prolonged(NonPlayableCharacter):
    def __init__(self):
        self.name = "Bowerick Wowbagger the Infinitely Prolonged"
        self.description = "Wowbagger is quite tall and has a peculiar flattened head. He has slitty alien eyes, golden robes with a peculiar collar design and pale grey-green skin that has a lustrous shine. He has thin spindly alien hands."
        self.gold = 0
        self.inventory =  []

class Effrafax(NonPlayableCharacter):
    def __init__(self):
        self.name = "Effrafax of Wug"
        self.description = "Effrafax of Wug was an ultrafamous sciento-magician who once bet his life that, given a year, he could render the great megamountain Magramal entirely invisible. Having spent most of the year jiggling around with immense Lux-O-Valves and Refracto-Nullifiers and Spectrum-By-Pass-O-Matics, he realized, with nine hours to go, that he wasn’t going to make it. So, he and his friends, and his friends’ friends, and his friends’ friends’ friends, and his friends’ friends’ friends’ friends, and some rather less good friends of theirs who happened to own a major stellar trucking company, put in what is now widely recognized as being the hardest night’s work in history and, sure enough, on the following day, Magramal was no longer visible. Effrafax lost his bet – and therefore his life – simply because some pedantic adjudicating official noticed (a) that when walking around the area where Magramal ought to be he didn’t trip over or break his nose on anything, and (b) a suspicious looking extra moon. If Effrafax had painted the mountain pink and erected a cheap and simple Somebody Else’s Problem field on it, then people would have walked past the mountain, around it, even over it, and simply never have noticed that the thing was there."
        self.gold = 0
        self.inventory =  [items.Sep(),
                        items.Ats()]

class Stylite(NonPlayableCharacter):
    def __init__(self):
        self.name = "Stylite"
        self.description = " "
        self.gold = 0
        self.inventory = []