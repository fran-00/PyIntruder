# MODULO DEI NEMICI

class Enemy:
    def __init__(self):
        raise NotImplementedError("Do not create raw Enemy objects.")

    def __str__(self):
        return self.name, self.hp

    def is_alive(self):
        return self.hp > 0

# Nemici Tier 1/5: da 1 a 25 DMG
class GelCube(Enemy):
    def __init__(self):
        self.name = "Gelatinous Cube"
        self.alive = True
        self.hp = 20
        self.damage = 10
        self.intro_alive = "A jelly-like cube wants to encompass you!"
        self.intro_dead = "Now the jelly is just a bunch of wet goo."
        self.look_alive = "He is big and jelly."
        self.look_dead = "Of him remaains only a bunch of slime."
        self.talk_alive = "<< BLBLBLBLBLBLBLBLBLBLBLBLBL >>"
        self.talk_dead = "A dead cube has nothing to say."

class Squirrel(Enemy):
    def __init__(self):
        self.name = "Ravenous Squirrel"
        self.alive = True
        self.hp = 40
        self.damage = 20
        self.intro_alive = "An angry squirrel wants to bite your carotid artery!"
        self.intro_dead = "You defeated a squirrel! That's something to be proud of."
        self.look_alive = "He's scary."
        self.look_dead = "It's horrible and dead."
        self.talk_alive = "<< GRRRRRRRRRRRRR >>"
        self.talk_dead = "<<...>>"

class Helicopter(Enemy):
    def __init__(self):
        self.alive = True
        self.name = "Helicopter"
        self.hp = 50
        self.damage = 25
        self.intro_alive = "A helicopter flies at you at full throttle."
        self.intro_dead = "The helicopter, now silent, is revealed to have been a mountain gadfly."
        self.look_alive = "EWWWWWWWWWWWW... GROSS."
        self.look_dead = "Ewww... gross."
        self.talk_alive = "<< BZZZZZZZZZZZZZZZZZZZZZZ >>"
        self.talk_dead = "Were the buzzes you've heard so far not enough for you?"

# Nemici Tier 2/5: da 30 a 45 DMG
class MushroomHunter(Enemy):
    def __init__(self):
        self.alive = True
        self.name = "Mushroom Hunter"
        self.hp = 60
        self.damage = 30
        self.intro_alive = "A mushroom hunter walking around with a wicker basket looks at you in a puzzled way, could he have understood that you are on drugs?"
        self.intro_dead = "The mushroom hunter returns to focus on mushrooms."
        self.look_alive = "Yes, he sure knows you are on drugs."
        self.look_dead = "Everyone knows that a mushroom hunter should be concerned with finding mushrooms and not disturbing people ON mushrooms."
        self.talk_alive = "<< Hi! >>"
        self.talk_dead = "He is too focused on identifying a mushroom."

class Cops(Enemy):
    def __init__(self):
        self.name = "Quad Biking Cops"
        self.alive = True
        self.hp = 80
        self.damage = 40
        self.intro_alive = "The cops are looking for carriers of joints and zozza."
        self.intro_dead = "ACAB!!!"
        self.look_alive = "Their blue lights are blinding."
        self.look_dead = "The only good quod cop is a dead quod cop. (I dissociate myself from that)."
        self.talk_alive = "<< Hands up and let yourself be searched. >>"
        self.talk_dead = "There are no more cops around here."

# Nemici Tier 3/5: da 50 a 65 DMG
class Bug(Enemy):
    def __init__(self):
        self.name = "Bug in the Program"
        self.alive = True
        self.hp = 100
        self.damage = 50
        self.intro_alive = "A mighty bug in the program threatens to stop the game so you don t win."
        self.intro_dead = "The code runs smoothly."
        self.look_alive = "It looks like Missingno."
        self.look_dead = "We will be rostoring normality as long as we are sure of what is normal anyway. Thank you."
        self.talk_alive = "<< You didn't put a bracket right there!!! >>"
        self.talk_dead = "There are no more bugs around here."

class Eyes(Enemy):
    def __init__(self):
        self.name = "Floating Eyes"
        self.alive = True
        self.hp = 110
        self.damage = 55
        self.intro_alive = "A swarm of floating eyes surrounds you and judges you severely. "
        self.intro_dead = "And now all eyes are closed. "
        self.look_alive = "They judge you without mercy. "
        self.look_dead = ">n eye never dies, but it closes and goes to bed."
        self.talk_alive = "<< We see everything. >>"
        self.talk_dead = "<< We are closed. Try again later. >>"

class Ants(Enemy):
    def __init__(self):
        self.name = "ants infected by a fungus"
        self.alive = True
        self.hp = 120
        self.damage = 60
        self.intro_alive = "Ophiocordyceps unilateralis suddenly attacks you riding on a herd of ants of the species Camponotus leonardi."
        self.intro_dead = "Eww... gross."
        self.look_alive = "Eww... gross."
        self.look_dead = "Eww... gross."
        self.talk_dead = "<< WE ARE LEGION. Resisting is useless. >>"
        self.talk_dead = "<< We'll be back. >>"

class Trog(Enemy):
    def __init__(self):
        self.name = "Trog"
        self.alive = True
        self.hp = 130
        self.damage = 65
        self.intro_alive = "A dog comes out from behind a tree and attacks you! Wait, so it's not just a dog... it's a Trog!"
        self.intro_dead = "The dog ran away. It can be said that the trog is no more."
        self.look_alive = "This Trog looks very pissed off. Is it hungry?"
        self.look_dead = "There are no more trogs here!"
        self.talk_alive = "<< GRRRRRRRRRRRRRRR! >>"
        self.talk_dead = " ..."


# Nemici Tier 4/5: da 70 a 85 DMG
class UncannyValley(Enemy):
    def __init__(self):
        self.name = "Uncanny Valley"
        self.alive = True
        self.hp = 140
        self.damage = 70
        self.intro_alive = "A robot which is almost, but not quite, entirely unlike humans confronts you!"
        self.intro_dead = "There are leaky cables everywhere."
        self.look_alive = "Ewwwwww... gross..."
        self.look_dead = "The scary AI is gone."
        self.talk_alive = "<< Remember before when I was talking about smelly garbage standing around being useless? That was a metaphor. I was actually talking about you. >>"
        self.talk_dead = "<< That thing you burned up isn't important to me. It's the fluid catalytic cracking unit. It made shoes for orphans. >>"

class Paranoia(Enemy):
    def __init__(self):
        self.name = "Paranoia"
        self.alive = True
        self.hp = 150
        self.damage = 75
        self.intro_alive = "You feel a sense of unbereable paraoia"
        self.intro_dead = "Now you feel way better."
        self.look_alive = "You can't see very weel, you feel very dizzy."
        self.look_dead = "Now threes looks greener."
        self.talk_alive = "<< ZZZZZZZZZ >>"
        self.talk_dead = "You hear the wind that moves the leaves and feel refreshed."

class Gnome(Enemy):
    def __init__(self):
        self.name = "Gnome armed with an ax"
        self.alive = True
        self.hp = 160
        self.damage = 80
        self.intro_alive = "OH MY GOD! It's a gnome armed with an ax!!!"
        self.intro_dead = "This terrifying abomination is no longer the terrible threat it was before."
        self.look_alive = "The argentines are hiking in a north american wood when they spot a strange figure in the distance. They approach to find out if it is an animal, continuing to wonder what it is. The girl throws a stone at him, suddenly the figure gets up: it is a gnome armed with an ax who begins to chase the tourists who are fleeing!!!"
        self.look_dead = " "
        self.talk_alive = " "
        self.talk_dead = " "

# Nemici Tier 5/5: da 100 a 105 DMG
class Herobrine(Enemy):
    def __init__(self):
        self.name = "Herobrine"
        self.alive = True
        self.hp = 180
        self.damage = 90
        self.intro_alive = " "
        self.intro_dead = " "
        self.look_alive = "Fine, Herobrine is real, and he gains spooky vengeance haunting power whenever you remind me of him. Only way to stop him is to ignore him."
        self.look_dead = " "
        self.talk_alive = " "
        self.talk_dead = " "

class RubberJohnny(Enemy):
    def __init__(self):
        self.name = "Rubber Johnny"
        self.alive = True
        self.hp = 190
        self.damage = 95
        self.intro_alive = "Johnny snorts a large line of zozza and begins to come towards you!"
        self.intro_dead = " "
        self.look_alive = " "
        self.look_dead = " "
        self.talk_alive = "<< Ma-ma...Ma-ma... >> "
        self.talk_dead = " "

class ArmillariaOstoyae(Enemy):
    def __init__(self):
        self.name = "Armillaria Ostoyae"
        self.alive = True
        self.hp = 200
        self.damage = 100
        self.intro_alive = "An immanent manifestation of the transcendent Armillaria ostoyae blocks your path."
        self.intro_dead = "Armillaria ostoyae stares silently at you from the Underground."
        self.look_alive = "Oh my God, she's HUGE."
        self.look_dead = "Even if you have defeated her, she still scares you."
        self.talk_alive = "<< I THINK, THEREFORE I AM >>"
        self.talk_dead = "<< I'M STILL HERE, TRAVELER. >>"


# ENEMIES FOR THE PATH
class BT(Enemy):
    def __init__(self):
        self.name = "BT"
        self.alive = True
        self.hp = 100
        self.damage = 100
        self.intro_alive = "A mighty BT wants to drive you crazy!"
        self.intro_dead = " "
        self.look_alive = " "
        self.look_dead = " "
        self.talk_alive = " "
        self.talk_dead = " "

class APS(Enemy):
    def __init__(self):
        self.name = "At His Own Expense"
        self.alive = True
        self.hp = 60
        self.damage = 50
        self.intro_alive = "It seems that this person is willing to publish a book at his own expense"
        self.intro_dead = " "
        self.look_alive = " "
        self.look_dead = " "
        self.talk_alive = " "
        self.talk_dead = " "

class FlatEarth(Enemy):
    def __init__(self):
        self.name = "The Earth is flat"
        self.alive = True
        self.hp = 60
        self.damage = 50
        self.intro_alive = " "
        self.intro_dead = " "
        self.look_alive = " "
        self.look_dead = " "
        self.talk_alive = " "
        self.talk_dead = " "

class WooWoo(Enemy):
    def __init__(self):
        self.name = "Pissed off Seagull"
        self.alive = True
        self.hp = 100
        self.damage = 25
        self.intro_alive = "An evil seagull appears from above the trees and attacks!"
        self.intro_dead = "The evil seagull has been defeated, now its beak is no longer a threat. "
        self.look_alive = "And I can't, because they attack "
        self.look_dead = " "
        self.talk_alive = " "
        self.talk_dead = " "

class Thief(Enemy):
    def __init__(self):
        self.name = "Hooded Thief"
        self.alive = True
        self.hp = 200
        self.damage = 90
        self.intro_alive = "A hooded thief wants to stab you in your sleep!"
        self.intro_dead = "The thief ran away."
        self.look_alive = "The thief is wrapped in a black cloak with a long hood covering his face"
        self.look_dead = " "
        self.talk_alive = "<< I will kill you... and all your treasures will be mine...>> "
        self.talk_dead = "..."