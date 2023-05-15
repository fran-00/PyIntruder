import random

from .templates import Armor, Curse, Enemy, Healer, ManaRecharger, MissionRelatedItem, NonPlayableCharacter, Surrounding, Trader, Weapon


class Factory:

    def get_entities_list(self, cls=None) -> list:
        if cls is None:
            return list(self.__dict__.values())
        else:
            return [entity for entity in self.__dict__.values() if isinstance(entity, cls)]


class ItemsFactory(Factory):

    def __init__(self):
        self.rinas_armor = Armor("Rina's Armor", 10)
        self.fungine_armor = Armor("Fungine Armor", 20)
        self.iron_armor = Armor("Iron Armor", 30)
        self.tesla_armor = Armor("Tesla Armor", 40)

        self.red = Curse("Self-Luminous Red", 5)
        self.hyperbolic_orange = Curse("Hyperbolic Orange", 10)
        self.stygian_blue = Curse("Stygian Blue", 15)
        self.discourse = Curse("Discourse on the Method", 20)
        self.falsidical = Curse("Falsidical Paradox", 25)
        self.cluster_point = Curse("Cluster Point", 30)
        self.aleph = Curse("Aleph Naught", 35)
        self.logistic_map = Curse("Logistic Map", 40)
        self.integral = Curse("Integral Of a Real Multivariate Function", 45)
        self.veridical = Curse("Veridical Paradox", 50)
        self.comic_sans = Curse("Comic Sans", 55)
        self.sep = Curse("Somebody Else's Problem Field", 60)
        self.nimby = Curse("NIMBY", 65)
        self.choice = Curse("Axiom of Choice", 70)
        self.antinomy = Curse("Antinomy", 75)
        self.continuum = Curse("Continuum Hypothesis", 80)
        self.insult = Curse("Ultimate Insult", 85)
        self.briefcase = Curse("Briefcase", 90)
        self.riemann = Curse("Riemann zeta function", 95)

        self.ats = Healer("Advanced Tea Substitute", 10)
        self.gommo = Healer("Gommo", 20)
        self.yellow_liquid = Healer("Suspicious Yellow Liquid", 30)
        self.golden_apple = Healer("Golden Apple", 40)
        self.nuka_cola = Healer("Nuka Cola", 50)
        self.bandages = Healer("Bandages", 60)
        self.gummy_bears = Healer("Gummy Bears", 70)
        self.mushrooms = Healer("Mushrooms", 80)

        self.plasma_pop = ManaRecharger("Plasma Pop", 10)
        self.dialectic_draught = ManaRecharger("Dialectic Draught", 20)
        self.fractal_fizz = ManaRecharger("Fractal Fizz", 30)
        self.neural_network = ManaRecharger("Neural Network", 140)
        self.schrodinger_solution = ManaRecharger("Schrodinger's Solution", 50)
        self.descartes_doubt = ManaRecharger("Descartes' Doubt", 60)

        self.specimen = MissionRelatedItem("The Specimen")
        self.bottle = MissionRelatedItem("bottle", openable=True)

        self.manuport = Weapon("Manuport", 5)
        self.sheet = Weapon("polarized sheet", 10)
        self.polyhedron = Weapon("Sharp Polyhedron", 15)
        self.armored_manuport = Weapon("Armored Manuport", 20)
        self.polygon = Weapon("Transparent Polygon", 25)
        self.wire = Weapon("Wireless Wire", 30)
        self.branch = Weapon("Armored Brench", 35)
        self.poly = Weapon("N-dimensional Polytope", 40)
        self.device = Weapon("Aperture Science Handheld Portal Device", 45)
        self.deliverance = Weapon("Deliverance", 50)
        self.tesseract = Weapon("Tesseract", 55)
        self.chuck = Weapon("Chuck the plant", 60)
        self.attractor = Weapon("Great Attractor", 65)
        self.cube = Weapon("The Soul Cube", 70)


class EntitiesFactory(Factory):
    def __init__(self):
        self.gel_cube = Enemy("Gelatinous Cube", 1, 20, 10)
        self.squirrel = Enemy("Ravenous Squirrel", 1, 30, 15)
        self.helicopter = Enemy("Helicopter", 1, 40, 20)
        self.hunter = Enemy("Mushroom Hunter", 2, 50, 25)
        self.bug = Enemy("Bug in the Code", 2, 60, 30)
        self.eyes = Enemy("Floating Eyes", 3, 70, 35)
        self.ants = Enemy("Ants infected by a Fungus", 3, 80, 40)
        self.trog = Enemy("Trog", 3, 90, 45)
        self.uncanny = Enemy("Uncanny Valley", 4, 100, 50)
        self.gnome = Enemy("Gnome armed with an ax", 4, 120, 60)
        self.ostoyae = Enemy("Armillaria Ostoyae", 5, 150, 75)

        self.littleo = Trader("Little(o)", [], Curse)
        self.blacksmith = Trader("Blacksmith", [], Weapon)
        self.innkeeper = Trader("Innkeeper", [], Healer)
        self.monk = Trader("Monk", [], ManaRecharger)
        self.merchant = Trader("Merchant", [], None)

        self.ferns = NonPlayableCharacter("Ferns", [])
        self.rina = NonPlayableCharacter("Rina", [])
        self.intruder = NonPlayableCharacter("Intruder", [])
        self.oak = NonPlayableCharacter("Oak", [])
        self.enzopaolo = NonPlayableCharacter("Enzo Paolo", [])
        self.priamo = NonPlayableCharacter("Priamo", [])
        self.effrafax = NonPlayableCharacter("Effrafax", [])
        self.stylite = NonPlayableCharacter("Stylite", [])

        self.car = Surrounding("car", [ItemsFactory().bottle], openable=True)
        self.chest = Surrounding("chest", [], openable=True)
        self.table = Surrounding("wooden table", [])
