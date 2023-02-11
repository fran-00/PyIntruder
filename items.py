import random

# >>>>> *** WEAPONS ***
class Weapon:
    def __init__(self):
        raise NotImplementedError("Do not create raw Weapon objects")

    def __str__(self):
        return f"{self.name} ({self.damage} DMG)"

# due in meno della metà, due in più della meta del danno. aggiungi la possibilità che le armi si rompano
class Manuport(Weapon):
    def __init__(self):
        self.name = "potential manuport"
        self.description = "It looks like this rock wants a passage. As long as you keep it with you, it will protect you."
        self.damage = 10
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(1000, 1100)
        self.if_sold = self.value // 100
        self.weight = 0

class Chick(Weapon):
    def __init__(self):
        self.name = "rubber chicken with a pulley in the middle"
        self.description = ""
        self.damage = 15
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(1200, 1300)
        self.if_sold = self.value // 100
        self.weight = 0

class Sheet(Weapon):
    def __init__(self):
        self.name = "polarized sheet"
        self.description = "It's a polarized sheet. It shows Fattuzu in light."
        self.damage = 20
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(1300, 1400)
        self.if_sold = self.value // 100
        self.weight = 0

class Polyhedron(Weapon):
    def __init__(self):
        self.name = "sharp polyhedron"
        self.description = "You should never leave your house without a sharp polyhedron in your pocket."
        self.damage = 25
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(1400, 1500)
        self.if_sold = self.value // 100
        self.weight = 0

class Manuport2(Weapon):
    def __init__(self):
        self.name = "armored manuport"
        self.description = "<< I'm a hitchhiker, can you give me a lift... please? >>"
        self.damage = 30
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(1500, 1600)
        self.if_sold = self.value // 100
        self.weight = 0

class Polygon(Weapon):
    def __init__(self):
        self.name = "transparent polygon"
        self.description = "Splits light into colored beams that blind enemies. Polarized sunglasses recommended."
        self.damage = 35
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(1600, 1700)
        self.if_sold = self.value // 100
        self.weight = 0

# Armi Tier 2: da 40 a 69 DMG
class Wire(Weapon):
    def __init__(self):
        self.name = "wireless wire"
        self.description = "Hmmm... "
        self.damage = 40
        self.mana_cost = None
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(1700, 1800)
        self.if_sold = self.value // 100
        self.weight = 0

class Branch(Weapon): #don't like
    def __init__(self):
        self.name = "armored brench"
        self.description = "It looks the same as any armored branch you've seen before. It hurts a lot when used with dexterity."
        self.damage = 45
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(1800, 1900)
        self.if_sold = self.value // 100
        self.weight = 0

class Polytope(Weapon):
    def __init__(self):
        self.name = "n-dimensional polytope"
        self.description = "Hummm..."
        self.damage = 50
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(1900, 2000)
        self.if_sold = self.value // 100
        self.weight = 0

class Chainsaw(Weapon):
    def __init__(self):
        self.name = "chainsaw (with no fuel)"
        self.description = "Excessively heavy."
        self.damage = 55
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(2000, 2100)
        self.if_sold = self.value // 100
        self.weight = 0

class CutlassOfKaflu(Weapon):
    def __init__(self):
        self.name = "Cutlass of Kaflu"
        self.description = ""
        self.damage = 60
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(2100, 2200)
        self.if_sold = self.value // 100
        self.weight = 0

class HandheldPortalDevice(Weapon):
    def __init__(self):
        self.name = "Aperture Science Handheld Portal Device"
        self.description = "It looks like the Zero Point Energy Field Manipulator but besides lifting things it opens portals... Of course it doesn't work, but you can effectively slam it into things."
        self.damage = 65
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(2200, 2300)
        self.if_sold = self.value // 100
        self.weight = 0

class Deliverance(Weapon):
    def __init__(self):
        self.name = "Deliverance by Tediore (Shotgun)"
        self.description = "Allow me to deliver my bullet to your head."
        self.damage = 70
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(2300, 2400)
        self.if_sold = self.value // 100
        self.weight = 0

class Tesseract(Weapon):
    def __init__(self):
        self.name = "tesseract"
        self.description = "Is an Optical Character Recognition tool. That is, it will recognize and read the text embedded in images. Did you think it was a deadly weapon like in The Cube?"
        self.damage = 75
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(2400, 2500)
        self.if_sold = self.value // 100
        self.weight = 0

class ChuckThePlant(Weapon):
    def __init__(self):
        self.name = "Chuck the plant"
        self.description = "red harring since 1987"
        self.damage = 80
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(2500, 2600)
        self.if_sold = self.value // 100
        self.weight = 0

class x(Weapon):
    def __init__(self):
        self.name = ""
        self.description = ""
        self.damage = 85
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(2600, 2700)
        self.if_sold = self.value // 100
        self.weight = 0

class GreatAttractor(Weapon):
    def __init__(self):
        self.name = "great attractor"
        self.description = "It's a gravitational anomaly in intergalactic space and the apparent central gravitational point of the Laniakea Supercluster."
        self.damage = 90
        self.mana_cost = None
        self.defence = None
        self.mr = None
        self.heal = None
        self.value = random.randint(2700, 2800)
        self.if_sold = self.value // 100
        self.weight = 0

class x(Weapon):
    def __init__(self):
        self.name = ""
        self.description = ""
        self.damage = 95
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(2800, 2900)
        self.if_sold = self.value // 100
        self.weight = 0

class SoulCube(Weapon):
    def __init__(self):
        self.name = "The Soul Cube"
        self.description = "Is an ancient Martian artifact and the most powerful weapon in Doom 3."
        self.damage = 100
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(2900, 3000)
        self.if_sold = self.value // 100
        self.weight = 0

# >>>>> *** CURSES ***
class Curse:
    def __init__(self):
        raise NotImplementedError("Do not create raw Curses objects")

    def __str__(self):
        return f"{self.name} ({self.damage} DMG)"

# il prezzo è più alto rispetto alle armi. dmg +- 3
class SelfLuminousRed(Curse):
    def __init__(self):
        self.name = "self-luminous red"
        self.description = "It's the impossible version of red."
        self.damage = random.randint(5, 15)
        self.mana_cost = 5
        self.defence = None
        self.mr = None
        self.heal = None
        self.value = random.randint(1000, 1200)
        self.if_sold = self.value // 100
        self.weight = 0

class HyperbolicOrange(Curse):
    def __init__(self):
        self.name = "hyperbolic orange"
        self.description = "It's the impossible version of orange."
        self.damage = random.randint(10, 20)
        self.mana_cost = 7
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(1100, 1300)
        self.if_sold = self.value // 100
        self.weight = 0

class StygianBlue(Curse):
    def __init__(self):
        self.name = "stygian blue"
        self.description = "It's the impossible version of blue."
        self.damage = random.randint(15, 25)
        self.mana_cost = 10
        self.defence = None
        self.mr = None
        self.heal = None
        self.value = random.randint(1200, 1400)
        self.if_sold = self.value // 100
        self.weight = 0

class Method(Curse):
    def __init__(self):
        self.name = "Discourse on the Method of Rightly Conducting One's Reason and of Seeking Truth in the Sciences"
        self.description = "<< Car ce n'est pas assez d'avoir l'esprit bon, mais le principal est de l'appliquer bien.>>"
        self.damage = random.randint(20, 30)
        self.mana_cost = 12
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(1300, 1500)
        self.if_sold = self.value // 100
        self.weight = 0

class Falsidical(Curse):
    def __init__(self):
        self.name = "falsidical paradox"
        self.description = "Packs a surprise, but it is seen as a false alarm when we solve the underlying fallacy. Good for Easy Enemies."
        self.damage = random.randint(25, 35)
        self.mana_cost = 15
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(1400, 1600)
        self.if_sold = self.value // 100
        self.weight = 0

class ClusterPoint(Curse):
    def __init__(self):
        self.name = "cluster point"
        self.description = "A Cluster point of a set S in a topological space X is a point x that can be approximated by points of S: every neighbourhood of x also contains a point of S other than x itself. A limit point of a set S does not itself have to be an element of S."
        self.damage = random.randint(30, 40)
        self.mana_cost = 17
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(1500, 1700)
        self.if_sold = self.value // 100
        self.weight = 0

class Godel(Curse):
    def __init__(self):
        self.name = "Gödel's completeness theorem for first-order predicate calculus"
        self.description = "Every syntactically consistent, countable first-order theory has a finite or countable model. This establishes a correspondence between semantic truth and syntactic provability in first-order logic: Gödel proved that first order logic is semantically complete but it is not syntactically complete, since there are sentences expressible in the language of first order logic that can be neither proved nor disproved from the axioms of logic alone."
        self.damage = random.randint(35, 45)
        self.mana_cost = 20
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(1600, 1800)
        self.if_sold = self.value // 100
        self.weight = 0

class AlephNaught(Curse):
    def __init__(self):
        self.name = "Aleph Naught"
        self.description = "Cardinality of Reals. You see, the cartesian product of a countable number of countable set is uncountable."
        self.damage = random.randint(40, 50)
        self.mana_cost = 22
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(1700, 1900)
        self.if_sold = self.value // 100
        self.weight = 0

class LogisticMap(Curse):
    def __init__(self):
        self.name = "Logistic Map"
        self.description = "Is a polynomial mapping of degree 2, often cited as an archetypal example of how complex, chaotic behaviour can arise from very simple non-linear dynamical equations."
        self.damage = random.randint(45, 55)
        self.mana_cost = 25
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(1800, 2000)
        self.if_sold = self.value // 100
        self.weight = 0

class Calculus(Curse):
    def __init__(self):
        self.name = "integral of a real multivariate function"
        self.description = "A function of several real variables is a function with more than one argument, the input variables take real values, while the output may be real or complex. "
        self.damage = random.randint(50, 60)
        self.mana_cost = 27
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(1900, 2100)
        self.if_sold = self.value // 100
        self.weight = 0

class Veridical(Curse):
    def __init__(self):
        self.name = "veridical paradox"
        self.description = "Packs a surprise, but the surprise quickly dissipates itself as we ponder the proof. Good for Medium enemies. "
        self.damage = random.randint(55, 65)
        self.mana_cost = 30
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(2000, 2200)
        self.if_sold = self.value // 100
        self.weight = 0

class ComicSans(Curse):
    def __init__(self):
        self.name = "Comic Sans"
        self.description = "If you love it, you don't know much about typography. If you hate it, you really don't know much about typography either, and you should get another hobby."
        self.damage = random.randint(60, 70)
        self.mana_cost = 32
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(2100, 2300)
        self.if_sold = self.value // 100
        self.weight = 0

class Sep(Curse):
    def __init__(self):
        self.name = "Somebody Else's Problem Field"
        self.description = "A SEP is something we can't see, or don't see, or our brain doesn't let us see, because we think that it's Somebody Else's Problem. The brain just edits it out, it's like a blind spot."
        self.damage = random.randint(65, 75)
        self.mana_cost = 35
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(2200, 2400)
        self.if_sold = self.value // 100
        self.weight = 0

class Nimby(Curse):
    def __init__(self):
        self.name = "not in my back yard"
        self.description = "Anywhere, but not in my back yard."
        self.damage = random.randint(70, 80)
        self.mana_cost = 37
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(2300, 2500)
        self.if_sold = self.value // 100
        self.weight = 0

class Analysis(Curse):
    def __init__(self):
        self.name = "Non-Standard Analysis"
        self.description = "Forget about the infinitesimal. (se equipaggiato, il piccol non è presente nella mappa o non è accessibile."
        self.damage = random.randint(75, 85)
        self.mana_cost = 40
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(2400, 2600)
        self.if_sold = self.value // 100
        self.weight = 0

class Choice(Curse):
    def __init__(self):
        self.name = "Axiom of Choice"
        self.description = "The cartesian product of non-empty sets is non-empty. Caution: may raise paradoxes."
        self.damage = random.randint(85, 95)
        self.mana_cost = 42
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(2500, 2700)
        self.if_sold = self.value // 100
        self.weight = 0

class Antinomy(Curse):
    def __init__(self):
        self.name = "antinomy"
        self.description = "Packs a surprise that can be accomodated by nothing less than a repudiation of part of our conceptual heritage. This is tough."
        self.damage = random.randint(90, 100)
        self.mana_cost = 45
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(2600, 2800)
        self.if_sold = self.value // 100
        self.weight = 0

class Continuum(Curse):
    def __init__(self):
        self.name = "continuum hypothesis"
        self.description = "There is no set whose cardinality is strictly between that of the integers and the real numbers."
        self.damage = random.randint(95, 105)
        self.mana_cost = 47
        self.defence = None
        self.mr = None
        self.heal = None
        self.value = random.randint(2700, 2900)
        self.if_sold = self.value // 100
        self.weight = 0

class UltimateInsult(Curse):
    def __init__(self):
        self.name = "Ultimate Insult"
        self.description = "Capable of crippling even the toughest pirate's ego."
        self.damage = random.randint(100, 110)
        self.mana_cost = 47
        self.defence = None
        self.mr = None
        self.heal = None
        self.value = random.randint(2800, 3000)
        self.if_sold = self.value // 100
        self.weight = 0

class MTheory(Curse):
    def __init__(self):
        self.name = "M-Theory"
        self.description = "It's a theory in physics that unifies all consistent versions of superstring theory."
        self.damage = random.randint(110, 120)
        self.mana_cost = 50
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(2900, 3100)
        self.if_sold = self.value // 100
        self.weight = 0

class Briefcase(Curse):
    def __init__(self):
        self.name = "Marcellus Wallace's briefcase"
        self.description = "<What's in the case?> <My boss's dirty laundry.> <Your boss makes you do his laundry?> <When he wants it cleaned.> <Sounds like a shit job.> <I was thinking the same thing.>"
        self.damage = random.randint(110, 120)
        self.mana_cost = 50
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(2900, 3100)
        self.if_sold = self.value // 100
        self.weight = 0

class Riemann(Curse):
    def __init__(self):
        self.name = "Riemann zeta function"
        self.description = "Full of trivial zeroes."
        self.damage = random.randint(110, 120)
        self.mana_cost = 50
        self.defence = None
        self.heal = None
        self.mr = None
        self.value = random.randint(3000, 3200)
        self.if_sold = self.value // 100
        self.weight = 0


# >>>>> *** CONSUMABLES ***
class Consumable:
    def __init__(self):
        raise NotImplementedError("Do not create raw Consumable objects.")

    def __str__(self):
        return f"{self.name} (+{self.heal} HP)"

# >>>>> *** HEALTH RECHARGERS ***
class Modification(Consumable):
    def __init__(self):
        self.name = "modification"
        self.description = "You could never live without it."
        self.damage = None
        self.defence = None
        self.heal = 10
        self.mr = None
        self.value = random.randint(100, 130)
        self.if_sold = self.value // 10
        self.weight = 0

class Bears(Consumable):
    def __init__(self):
        self.name = "bag with red gummy bears"
        self.description = "They are full of glucose, perfect for synthesizing ATP."
        self.damage = None
        self.defence = None
        self.heal = 20
        self.mr = None
        self.value = random.randint(130, 160)
        self.if_sold = self.value // 10
        self.weight = 0

class HomemadeCookies(Consumable):
    def __init__(self):
        self.name = "homemade cookies"
        self.description = "With chocolate or jelly."
        self.damage = None
        self.defence = None
        self.heal = 30
        self.mr = None
        self.value = random.randint(160, 190)
        self.if_sold = self.value // 10
        self.weight = 0

class Cappuccino(Consumable):
    def __init__(self):
        self.name = "Cappuccino"
        self.description = "Creamy and dense."
        self.damage = None
        self.defence = None
        self.heal = 35
        self.mr = None
        self.value = random.randint(190, 220)
        self.if_sold = self.value // 10
        self.weight = 0

class CremeCroissant(Consumable):
    def __init__(self):
        self.name = "Creme croissant"
        self.description = "Made by Picca Uda."
        self.damage = None
        self.defence = None
        self.heal = 40
        self.mr = None
        self.value = random.randint(220, 250)
        self.if_sold = self.value // 10
        self.weight = 0

class Blackberries(Consumable):
    def __init__(self):
        self.name = "blackberries"
        self.description = "The panna cotta IS the message."
        self.damage = None
        self.defence = None
        self.heal = 50
        self.mr = None
        self.value = random.randint(250, 280)
        self.if_sold = self.value // 10
        self.weight = 0

class Gommo(Consumable):
    def __init__(self):
        self.name = "gommo"
        self.description = "<< What are these atrocious grimaces?> << What grimaces? >> << These!>> << Which ones? >> << The ones you are doing with your crippled mouth! >> "
        self.damage = None
        self.defence = None
        self.heal = 60
        self.mr = None
        self.value = random.randint(280, 310)
        self.if_sold = self.value // 10
        self.weight = 0

class Ats(Consumable):
    def __init__(self):
        self.name = "Advanced Tea Substitute"
        self.description = "A liquid which is almost, but not quite, entirely unlike tea."
        self.damage = None
        self.defence = None
        self.heal = 70
        self.mr = None
        self.value = random.randint(310, 340)
        self.if_sold = self.value // 10
        self.weight = 0

class SusMushrooms(Consumable):
    def __init__(self):
        self.name = "Suspicious mushrooms"
        self.description = "These seemingly delicious mushrooms have a rather sus appearance..."
        self.damage = None
        self.defence = None
        self.heal = 80
        self.mr = None
        self.value = random.randint(340, 370)
        self.if_sold = self.value // 10
        self.weight = 0

class PannaCotta(Consumable):
    def __init__(self):
        self.name = "Panna Cotta"
        self.description = "The panna cotta IS the message."
        self.damage = None
        self.defence = None
        self.heal = 90
        self.mr = None
        self.value = random.randint(370, 400)
        self.if_sold = self.value // 10
        self.weight = 0

class Strudel(Consumable):
    def __init__(self):
        self.name = "Strudel"
        self.description = "Wooow"
        self.damage = None
        self.defence = None
        self.heal = 100
        self.mr = None
        self.value = random.randint(400, 430)
        self.if_sold = self.value // 10
        self.weight = 0

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
        return "{} ({} DEF)".format(self.name, self.defence)

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
        return "{} ".format(self.name)

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

