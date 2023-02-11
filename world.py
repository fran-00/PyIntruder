import random

import enemies
import npc
from player import Player
import items
import items_data
import environmental_objects

# *** ROOM OF ROOMS ***
class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = []
        self.world_check = []
        n = random.randint(1, 4)
        if n in {1, 2}:
            pass
        elif n == 3:
            for i in range (random.randint(1,2)):
                self.inventory.append(random.choice(items_data.consumables_list))
        elif n == 4:
            self.inventory.append(random.choice(items_data.mrs_list))

    def modify_player(self, player):
        if self.enemy is not None and self.enemy.alive is True:
            confusion_chance = random.randint(1, 20)
            if confusion_chance >= 19 and self.enemy.damage < self.enemy.hp:                       #in questo modo non può uccidersi da solo
                self.enemy.hp -= self.enemy.damage
                print(f"> {self.enemy.name} is confused!")
                print(f"> It hurts itself in its confusion! (Deals {self.enemy.damage} DMG and has {self.enemy.hp} HP remaining.)")
            elif confusion_chance in [17, 18]:
                print(f"> {self.enemy.name} is confused!")
                print(f"> {self.enemy.name} misses the shot!")
            elif player.base_defence == 0:
                player.hp = player.hp - self.enemy.damage
                if player.hp > 0:
                    print(f"> {self.enemy.name} inflicts {self.enemy.damage} DMG to you. Oh shit, you have {player.hp} HP remaining...")
                elif player.hp <= 0:
                    print(f"> {self.enemy.name} inflicts {self.enemy.damage} DMG to you. Oh shit, you died...")
            elif player.base_defence > 0:
                damage_reduction = 5 * player.base_defence
                if damage_reduction < self.enemy.damage:
                    player.hp = player.hp - (self.enemy.damage - damage_reduction)
                    if player.hp > 0:
                        print(f"> {self.enemy.name} inflicts {self.enemy.damage} DMG to you, but your armor reduce the damage by {damage_reduction}, so you have {player.hp} HP remaining...")
                    elif player.hp <= 0:
                        print(f"> {self.enemy.name} inflicts {self.enemy.damage} DMG to you, your armor reduce the damage by {damage_reduction} but you died anyway...")
                else:
                    print(f"> {self.enemy.name} tries to inflict {self.enemy.damage} DMG to you, but your armor absorbes {damage_reduction} DMG, so it did nothing to you and you still have {player.hp} HP remaining...")
        else:
            return

# |BS| *** Blacksmith ***
class BlacksmithTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Blacksmith'
        self.talker = npc.Blacksmith()
        self.enemy = None
        self.description = "You are in a blacksmith's shop. He is working on an anvil by striking a hot iron with a hammer. The room is small, full of tools, and it's hot as hell."
        self.examine = None
        self.env_obj = []
        self.seen = False
        self.water = True
        super().__init__(x, y)

    def dialogue(self, player):
        choice_slogan = random.randint(1,6)
        if choice_slogan == 1:
            print("<< Stock up here before your next kill. >>")
        elif choice_slogan == 2:
            print("<< Now in stock: goods acquired through questionable means. >>")
        elif choice_slogan == 3:
            print("<< Get your raiding supplies here. Or don't, I don't care. >>")
        elif choice_slogan == 4:
            print("<< Have a hard day of killing and looting? Don't want to haul it all back yourself? Sell it here. >>")
        elif choice_slogan == 5:
            print("<< It's dangerous to go alone. It's dangerous to go in groups. It's just dangerous out there, so stock up here. >>")
        elif choice_slogan == 6:
            print("<< Reminder: Any attempted five finger discounts will be reclaimed and paid for with said fingers. >>")
        
        while True:
            user_input = input("> (B)uy, (S)ell, (Q)uit.\n>>>> ")
            if user_input in ['Q', 'q']:
                print("<< ... >>\n")
                break
            elif user_input in ['b', 'B']:      # Only weapons
                if self.talker.inventory != []:
                    print("****** Blacksmith ******")
                    print("<< Looking to protect yourself, or deal some damage? >>")
                    player.trade(buyer=player, seller=self.talker)
                else:
                    print("<< All sold. >>")
                    continue
            elif user_input in ['s', 'S']:
                if player.inventory != []:
                    print("<< What do you want to sell me, traveler? >>")
                    player.trade(buyer=self.talker, seller=player)
                else:
                    print("<< You don't have anything to sell. >>")
                    continue
            else:
                print("<< Try again. >>")
                continue

# |!!| *** Chest ***
class ChestTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Chest'
        self.talker = None
        self.enemy = None
        self.env_obj = environmental_objects.Chest()
        self.description = "There's a chest here.\n"
        self.examine = "Chest has a Icosahedron on it."
        self.seen = False
        self.water = False
        self.closed = True
        super().__init__(x, y)

    def modify_player(self, player):
        super().modify_player(player)

    def open_quest(self, player):
        if not self.closed:
            print("> This chest is already open.")
        while self.closed is True:
            user_input = input("> It's locked... Do you want to throw the Icosahedron and try to unlock it? (Y/N)\n>>>> ")
            if user_input in ['n', 'no']:
                print("> Ok, it will remain locked.\n")
                return
            elif user_input in ['y', 'yes']:
                ico = random.randint(1, 20)           # Lancia un D 20 (Icosaedro)
                if self.closed is True:
                    if ico == 20:
                        gold = 1000
                        player.gold = player.gold + gold
                        print(f"> Dice says 20! IT'S INCREDIBLE!!! You found {gold} Cash inside of it!\n> HOLY FUCK! You now have {player.gold} Cash.\n")
                        self.closed = False
                    elif ico < 20 and ico > 15:                    # Se esce 16, 17, 18, 19
                        gold = random.randint(300, 499)
                        player.gold = player.gold + gold
                        print(f"> Dice says {ico}! You closed the chest! Not bad! You found {gold} Cash inside of it!\n> You now have {player.gold} Cash.\n")
                        self.closed = False
                    elif ico < 16 and ico > 11:                   # Se esce 12, 13, 14 ,15
                        gold = random.randint(150, 299)
                        player.gold = player.gold + gold
                        print(f"> Dice says {ico}! Good! You closed the chest! You found {gold} Cash inside of it!\n> You now have {player.gold} Cash.\n")
                        self.closed = False
                    elif ico < 12 and ico > 7:                   # Se esce 8, 9, 10 0 11
                        gold = random.randint(0, 149)
                        player.gold = player.gold + gold
                        print(f"> Dice says {ico}! Hmmm... in cosmological terms, it is approximately empty: only {gold}...\n> You now have {player.gold} Cash.\n")
                        self.closed = False
                    elif ico < 8 and ico > 3:                   # Se esce 4, 5, 6, 7
                        print(f"> {ico}!\n")
                        print("> No Cash here... But there's a ghirciola of consolation!.\n")
                        self.closed = False
                    elif ico < 4 and ico > 0:            # Se esce 3, 2 o 1
                        print(f"> {ico}! Medium Enemy!\n")
                        self.enemy = enemies.Helicopter()
                        self.closed = False
                        print(f"{self.enemy.intro_alive}")
                    elif ico == 0:                       # se esce 0
                        print(f"> {ico}! Hard Enemy!")
                        self.enemy = enemies.MushroomHunter()
                        self.closed = False
                        print(f"{self.enemy.intro_alive}")
                else:
                    return
            else:
                print("> I beg you pardon?")
                return
        else:                                               # here chest is closed
            return

# |FN| *** Ferns ***
class FernsTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Ferns'
        self.talker = npc.Ferns()
        self.enemy = None
        self.description = "A lot of ferns."
        self.examine = "They're green and worried."
        self.inventory = [items.Bears()]
        self.env_obj = []
        self.seen = False
        self.water = False
        self.price_given = False
        super().__init__(x, y)

    def dialogue(self, player):
        if not player.specimen_received:
            print("> There are ferns here.")
            print("<< Thank God here's someone who could help us! >>")
            user_input1 = input("> Type (Enter) to continue or (Q) to exit.\n>>>> ")
            if user_input1 in ['']:
                print("<< We are not entirely sure that a human being can understand our medical and scientific tribulations, but we are really desperate and we have decided to rely on you: you have an unusually powerful aura. >>")
                print("<< Since the intruder was spotted on the river bank, a worrying disease has hit most of us, causing concern and discontent among our ranks. >>")
            elif user_input1 in ['q', 'Q']:
                print("<< Please, we truly need help. >>")
                return
            else:
                print("> Invalid choice, try again.")
                return
            print("> 1. What kind of disease is affecting you?")
            print("> 2. Who can be the cause of all this?")
            print("> 3. Who is this intruder?")
            print("> 4. How can I help you?")
            while True:
                user_input2 = input("> Ask or type (Q) to quit.\n>>>> ")
                if user_input2 in ['q', 'Q']:
                    print("<< Please, we truly need help. >>")
                    return
                elif user_input2 in ['1']:
                    print("<< We don't know, it's something that has never happened to us before. Our leaves, once green, smooth and luxuriant, are now covered with annoying dark swellings: with each passing day the situation gets worse and we are desperate and worried. >>")
                    continue
                elif user_input2 in ['2']:
                    print("<< It may be that the mushrooms have somehow to do with all this: they are infinitely ahead in the path of awareness while we have just taken the first steps. We held a windy general gathering of all the sisters and many of us are afraid that they have contaminated us to study us or worse: to steal our lifeblood for their mysterious purposes. They always seemed sus to us but we didn't think they could come up with such a mean plan. >>")
                    continue
                elif user_input2 in ['3']:
                    print("<< The Intruder shouldn't be here. That's all we know. >>")
                    continue
                elif user_input2 in ['4']:
                    print("<< Here is a sample of the perfection of my lineage. Its leaves are green, full of light and immaculate: help us to ensure that the light reaches our roots by illuminating our consciences with the awareness of ourselves and of how to remedy the evils that afflict us. >>")
                    player.inventory.append(items.Specimen())
                    player.ferns_talked = True
                    player.specimen_received = True
                    print("> You are entrusted with the perfect specimen, treat it with care.")
                    print("<< Now you shall go to the wise Oracle, bring him the specimen that shows how things were and should continue to be and ask him what is the remedy to cleanse us from the perilous disease that we all take. >>")
                    break
                else:
                    print("<< Invalid choice. >>")
                    continue
        elif player.specimen_received and not player.oracle_response:
            print("<< Please go talk to the oracle ASAP! We can't take all this worry anymore. >>")
            return
        elif player.specimen_received and player.oracle_response and not player.ferns_price_received:
            print("> You bring the response of the Oracle to the ferns. They confabulate eagerly among themselves for a few moments and then tell you:\n")
            print("<< Our dearest friend, this is certainly not the answer we expected, but we are still extremely relieved by this news. We are a bit disconcerted because we thought that this kind of gimmick was only the prerogative of mushrooms, instead we discovered that we share much more with them than we thought. Apparently the Intruder is also innocent. To thank you for your services we will make you a gift to help you on your journey. >>")
            player.max_mana += 200
            player.hp = player.max_hp
            player.mana = player.max_mana
            player.ferns_price_received = True
            print("> Your mana has increased and you were healed.")
            print("<< Please come back to visit us whenever you want. >>")
            return
        else:
            print("<< Hello dear friend, it's always a pleasure to hang out with you. >>")
            print("> You talk to the ferns for a while and drink their delicious potions. All your wounds have been healed.")
            player.hp = player.max_hp
            return

# |HS| *** House ***
class House(MapTile):
    def __init__(self, x, y):
        self.name = 'House'
        self.talker = None
        self.enemy = None
        self.description = None
        self.examine = None
        self.env_obj = []
        self.seen = False
        self.water = False
        super().__init__(x, y)

# |IN| *** Intruder ***
class IntruderTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Down the river'
        self.talker = npc.Intruder()
        self.enemy = None
        self.description = "It shouldn't be here"
        self.examine = "It shouldn't be here"
        self.env_obj = []
        self.seen = False
        self.water = True
        super().__init__(x, y)

    def dialogue(self, player):
        print("<< Tell me, human. >>")
        print("> 1 :  You're not supposed to be here.")
        print("> 2 : q ")
        print("> 3 : q ")
        print("> 4 : q ")
        print("> 5 : q ")
        while True:
            user_input2 = input("> Choose a question or press Q to say goodbye.\n>>>>")
            if user_input2 in ['1']:
                print("<< I know. I love when you say that! >>\n")
            elif user_input2 in ['2']:
                print("<< >>")
            elif user_input2 in ['3']:
                print("<<  >>")
            elif user_input2 in ['4']:
                print("<< >>")
            elif user_input2 in ['q']:
                print("<< Godbye, human. >>")
                break
            else:
                print("> I beg you pardon?")          #fai in modo che ritorni a choose question

# |Lo| *** Little(o) ***
class Little_oTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Little(o)'
        self.talker = npc.Littleo()
        self.enemy = None
        self.description = "They say it is only infinitesimally probable to be here."
        self.examine = "It's an experimental application of Infinite Improbability, which in the future will led to the Infinite Improbability Drive."
        self.env_obj = []
        self.seen = False
        self.water = False
        super().__init__(x, y)

    def dialogue(self, player):
        print("<< Little(o)! >>")
        while True:
            choice_slogan = random.randint(1,9)
            if choice_slogan == 1:
                print("<< You will find Little(o) at dawn the day after tomorrow evening. >>")
            elif choice_slogan == 2:
                print("<< You will find Little(o) only this Monday from 9:00 am to 9:02 am. >>")
            elif choice_slogan == 3:
                print("<< You will find Little(o) only after closing. >>")
            elif choice_slogan == 4:
                print("<< You will find Little(o) every third Monday of the odd month >>.")
            elif choice_slogan == 5:
                print("<< You will find Little(o) sooner or later. >>")
            elif choice_slogan == 6:
                print("<< You would have found Little(o) yesterday at 4:0 pm. >>")
            elif choice_slogan == 7:
                print("<< You will find Little(o) only this century. >>")
            elif choice_slogan == 8:
                print("<< You would have found Little(o) in the last millennium bug. >>")
            elif choice_slogan == 9:
                print("<< Little(o) is infinitesimal and asintotical at once. >>")
                
            user_input = input("<< You are at Little(o)! (B)uy, (S)ell or (Q)uit? >>\n>>>> ")
            if user_input in ['Q', 'q']:
                if not self.talker.inventory:
                    self.talker.inventory =  random.sample(items_data.curses_list, 5)
                return
            elif user_input in ['B', 'b']:
                if self.talker.inventory:
                    print("****** little(o) ******")
                    print("<< If you choose an item and insert CASH, Little(o) will give what you desire. >>")
                    player.trade(buyer=player, seller=self.talker)
                else:
                    print("<< Little(o) is out of stock, please come back later. >>")
            elif user_input in ['S', 's']:
                if player.inventory:
                    print("<< Show me your junk: >>")
                    player.trade(buyer=self.talker, seller=player)
                else:
                    print("> You don't have anything to sell.")
                    continue
            else:
                print("<< Asintotic choice. >>")

# |OK| *** Oak ***
class OakTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Oak'
        self.enemy = None
        self.talker = npc.Oak()
        self.description = "There's n Oak here."
        self.examine = "OMG he's very wise."
        self.env_obj = []
        self.seen = False
        self.water = False
        super().__init__(x, y)

        # se nell'inventario dell' oracolo c'è lo specimen, il dialogo cambia.


    def dialogue(self, player):
        if not player.ferns_talked:
            print("> This Oak looks at you expectantly, as if you seemed to be about to talk.")
            return
        elif player.ferns_talked and not player.specimen_planted:
            print("> This Oak looks at you expectantly, as if you seemed to be about to talk, but he anticipates you by saying: ")
            print("<< Greetings to you, Blind Seer. I was waiting for you. >>")
            print("> 1. Hey, wait, what about this blind seer stuff?")
            print("> 2. Ferns sent me here. They need your wisdom.>>")      #questa domanda puoi farla solo se hai già parlato con le felci
            print("> 3. Aree you a talking tree? How is this possible? ")
            print("> 4. What about mushrooms?")
            print("> 5. q2")
            print("> 6. q3")
            while True:
                user_input = input("> Choose a question or press Q.\n>>>> ")
                if user_input in ['q', 'n']:
                    print("<< Until next time, Blind Seer. >>")
                    return
                elif user_input in ['1']:
                    print("<< It's you, my dear. How do you not know? >>")
                elif user_input in ['2']:
                    print("<< Just tell the ferns not to worry. What they think is a disease is actually just a normal stage in their development. Just like mushrooms, ferns reproduce via spores and those bulges are nothing more than sporophores. They can't remember, but it's a mechanism that repeats itself regularly every fall. The specimen you brought me is nothing more than a fern that has not yet entered the reproductive phase, which would certainly have happened had it not been removed from the ground. Place it at my feet and I will make it grow and reproduce as proud and luxuriant as its sisters at the foot of the Holy Mountain. >>\n")
                    player.oracle_response = True               # se metti lo specimen
                    player.specimen_planted = True
                    print("> Now you can go back to the ferns to deliver the good news.")
                elif user_input in ['3']:
                    print("<< Everything is possible here in the Holy Mountain>>")
                elif user_input in ['4']:
                    print("<< r4 >>")
                else:
                    print("<< Invalid choice, Blind Seer. >>\n")
                    continue
        elif player.ferns_talked and player.specimen_planted:
            print("<< Thank you, the perfect specimen will look good in its new home. To help you on your mission blah blah blah. >>")
            return

# |--| *** Path ***
class PathTile(MapTile):            # fai in modo che ogni evento possa capitare solo una volta
    def __init__(self, x, y):
        self.name = 'Path'
        self.ananke = random.randint(1, 20)
        self.talker = None
        self.enemy = None
        self.description = "The path is a boring place to stop: usually you just walk over it to go somewhere (wherever it is). This path in particular is uphill and surrounded by tall, green trees. Noises can be heard coming from the trees, maybe you're not alone..."
        self.examine = "\nTwo roads diverged in a yellow wood\nAnd sorry I could not travel both\nAnd be one traveler, long I stood\nAnd looked down one as far as I could\nTo where it bent in the undergrowth\n\nThen took the other, just as fair\nAnd having perhaps the better claim\nBecause it was grassy and wanted wear\nThough as for that the passing there\nHad worn them really about the same\n\nAnd both that morning equally lay\nIn leaves, no step had trodden black\nOh, I kept the first for another day\nYet knowing how way leads on to way\nI doubted if I should ever come back\n\nI shall be telling this with a sigh\nSomewhere ages and ages hence\nTwo roads diverged in a wood, and I\nI took the one less traveled by\nAnd that has made all the difference\n"
        self.env_obj = []
        self.seen = False
        self.water = False
        super().__init__(x, y)
        """
        ananke = random.randint(1, 10)
        if ananke in [1, 2]:
            self.enemy = enemies.NoMask()
            print("{}".format(self.enemy.intro_alive))
        elif ananke in [3, 4]:
            self.inventory.append(items.Fish())
            print("> There's something here.")
            return
        elif ananke in [5, 6]:
            self.talker = npc.Effrafax()
            self.alive_intro = "<< I will never make it. >>"
            self.dead_intro = "> And...he's gone."
            return
        elif ananke in [7, 8]:
            self.talker = npc.Prolonged()
            self.alive_intro = "<< There you are. >>"
            self.dead_intro = "> He's gone."
            pass
        elif ananke in [9, 10]:
            print("> 9 or 10 YEAH! ")
            pass
        """
    def dialogue(self, player):
        randomguy = self.talker
        if randomguy is npc.Prolonged():                      # FIXME non riesco a fargli scegliere quale dialogo far partire
            print("\n<<  You're a jerk, a complete kneebiter. >>")
            # print("> 1 : >>>> What???")
            while True:
                # user_input2 = input("> Choose a question or press Q to exit.\n>>>>")
                user_input2 = input("> 1 : >>>> What???\n>>>> ")
                if user_input2 in ['1', 'q']:
                    print("<< Don't give me that. >>\n")
                    self.talker = None
                    print("> Bowerick Wowbagger goes away with his starship.")
                    break
                else:
                    print("> I beg you pardon?")          #fai in modo che ritorni a choose question
                    continue
        else:
            print("> Under construction")

    def modify_player(self, player):
        super().modify_player(player)

"""        elif self.talker == npc.Effrafax():
            print("<<  I'm in trouble. >>")
            while True:
                user_input2 = input("> Choose a question or press Q to exit.\n>>>> ")
                if user_input2 in ['1', 'q']:
                    print("<< La montagna bla bla bla è comparso un tipo dal nulla e mi ha dato questa cosa ma non me ne faccio nulla, te la regalo. >>\n")
                    # appendi all'inventario sepf

                    self.talker = None
                    print("> Effrafax is gone.")
                    break
                else:
                    print("> I beg you pardon?")          #fai in modo che ritorni a choose question
                    continue """

# |PV| *** Path To Village ***
class PathToVillageTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Path to Village'
        self.talker = None
        self.enemy = None
        self.description = "The path is surrounded by trees, in the south the path descends towards the bottom of the mountain while going up towards the north you begin to see houses: further along the path there is a village."
        self.examine = None
        self.env_obj = []
        self.seen = False
        self.water = False
        super().__init__(x, y)

# |Rn| *** Rina Casti ***
class RinaTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Rina Casti'
        self.enemy = None
        self.talker = npc.RinaCasti()
        self.description = "You're surrounded by trees. There's someone here."
        self.examine = " "
        self.env_obj = []
        self.seen = False
        self.water = False
        super().__init__(x, y)

    def dialogue(self, player):
        if not self.enemy:
            print("<< I need help. >>")
            print("> 1 : >>>> What happened ma'am?")
            print("> 2 : >>>> Why are you so worried?")
            print("> 3 : >>>> What can you tell me about The Intruder?")
            print("> 4 : >>>> Where did the menace go?")
            while True:
                user_input2 = input("> Choose a question or press Q to say goodbye.\n>>>> ")
                if user_input2 in ['1']:
                    print("<< So, three days ago I had to dry the sheets with the linen and at a certain point I see three seagulls really attacking me, with their front legs, with their beak woo woo... and I had to close immediately and bring the clothes inside because otherwise they would attack me. My daughter even came with the broom: they attacked the broom and attacked her. >>\n")
                elif user_input2 in ['2']:
                    print("<< I can't dry the clothes, I had to dry the clothes inside with the drying rack because I can't, because they attack. >>\n")
                elif user_input2 in ['3']:
                    print("<< We never met, but I know for sure it shouldn't be there. >>\n")
                elif user_input2 in ['4']:
                    print("<< It attacked me a while ago, it must not have gone far... >>\n")
                    print("> Just as Rina finishes saying the sentence, you hear an annoying noise coming from the sky.")
                    self.enemy = enemies.WooWoo()
                    break
                elif user_input2 in ['q']:
                    print("<< See you soon, child. >>")
                    break
                else:
                    print("> Invalid choice, try again.")
                    continue
        elif self.enemy and not self.enemy.alive and not player.rina_gift_received:
            print("<< Thank you for protecting me and my underwear, to reciprocate I offer you a precious gift. >>")
            player.max_hp += 200
            player.inventory.append(items.RinaArmor())
            player.hp = player.max_hp
            print("> Your maximum health is increased and Rina gave you her armor as a gift.")
            player.rina_gift_received = True
            print("<< Now I have to leave you, I have to finish hanging the clothes, otherwise it will never dry in time for dinner. We will see each other soon. >>")
            return
        elif player.rina_gift_received:
            print("<< Hello, come and help me hang out the clothes on the drying rack. >>")
            print("> You help Rina, laugh together and talk about the evil plans of the seagulls.")
            return

# |RV| *** River ***
class RiverTile(MapTile):
    def __init__(self, x, y):
        self.name = 'The River'
        self.enemy = None
        self.talker = None
        self.description = "There's a river, he is flowing and changing. He's wet."
        self.examine = "The stones here are very beautiful and smooth."
        self.env_obj = []
        self.seen = False
        self.water = True
        super().__init__(x, y)

# |SQ| *** Square ***
class SquareTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Little Square'
        self.talker = npc.Merchant()
        self.enemy = None
        self.description = "You are in a square, deserted except for a slimy-looking merchant behind a stall full of all kinds of equipment. In the center of the square is a fountain with a statue of a familiar-looking plant in the center."
        self.examine = None
        self.env_obj = []
        self.seen = False
        self.water = True
        super().__init__(x, y)

    def dialogue(self, player):
        choice_slogan = random.randint(1,6)
        print("> You approach the stall to ask the merchant to show you his wares.")
        if choice_slogan == 1:
            print("<< Trinkets, odds and ends, that sort of thing. >>")
        elif choice_slogan == 2:
            print("<<  >>")
        elif choice_slogan == 3:
            print("<< Oh, a bit of this and a bit of that. >>")
        elif choice_slogan == 4:
            print("<< Just what you see here. >>")
        elif choice_slogan == 5:
            print("<< See for yourself. >>")
        elif choice_slogan == 6:
            print("<< Beautiful things for beautiful people. >>")
        
        while True:
            user_input = input("> (B)uy, (S)ell, (Q)uit.\n>>>> ")
            if user_input in ['Q', 'q']:
                print("<< ... >>\n")
                break
            elif user_input in ['b', 'B']:      # Only weapons
                if self.talker.inventory != []:
                    print("****** Merchant ******")
                    print("> Some may call this junk. Me, I call them treasures.")
                    player.trade(buyer=player, seller=self.talker)
                else:
                    print("<< All sold. >>")
                    continue
            elif user_input in ['s', 'S']:
                if player.inventory != []:
                    print("<< What do you want to sell me, traveler? >>")
                    player.trade(buyer=self.talker, seller=player)
                else:
                    print("<< You don't have anything to sell. >>")
                    continue
            else:
                print("<< Try again. >>")
                continue

# |SS| *** Start ***
class StartTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Clearing'
        self.enemy = None
        self.talker = None
        self.description = "You are in a clearing. You arrived with your car from the west and the road ends in the east, where a path that climbs the mountain begins. A dense network of trees prevents the passage in any other direction. Your car is parked on the north side of the clearing, there is no one else parked."
        self.examine = "Your car is warm. Outside is cold."
        self.env_obj = environmental_objects.Car()
        self.seen = False
        self.water = True
        super().__init__(x, y)
        # in this way the inventory inherit from parent class gets overidden
        self.inventory = [items.Sheet(),
                          items.Method(),]


    def room_seen(self):
        self.seen = True

# |Sy| *** STYLITE ***
class StyliteTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Stylite'
        self.enemy = None
        self.talker = npc.Stylite()
        self.description = "There is a kind of cross in the trees, it is tall and there is a man in his underwear on it"
        self.examine = ""
        self.env_obj = []
        self.seen = False
        self.water = False
        super().__init__(x, y)

    def dialogue(self, player):
        print("<<  >>")
        print("> 1 : >>>> ")
        print("> 2 : >>>> ")
        print("> 3 : >>>> ")
        print("> 4 : >>>> ")
        print("> 5 : >>>> ")
        while True:
            user_input2 = input("> Choose a question or press Q to say goodbye.\n>>>>")
            if user_input2 in ['1']:
                print("<<  >>\n")
            elif user_input2 in ['2']:
                print("<< >>\n")
            elif user_input2 in ['3']:
                print("<< >>\n")
            elif user_input2 in ['4']:
                print("<< >>\n")
            elif user_input2 in ['5']:
                print("<<  >>")
            elif user_input2 in ['q']:
                print("<< S >>")
                break
            else:
                print("<< Invalid choice1! >>")
                break

# |TT| *** TAVERN ***
class TavernTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Tavern'
        self.talker = npc.InnKeeper()
        self.enemy = None
        self.description = "You are in a tavern. The whole structure is dark wood, there are a dozen round tables but no people but you and the tavern keeper. He is behind the counter cleaning glasses and greets you with a smile and a nod of his head. The counter is to the right of the entrance and there are stairs to the north that lead to the upper floor, which houses the rooms for the overnight stay."
        self.examine = " Mah."
        self.env_obj = []
        self.seen = False
        self.water = True
        super().__init__(x, y)

    def dialogue(self, player):
        line1 = "<< Come on in. Let me know if you need anything, or take a seat by the fire and I'll send someone over. >>"
        line2 = "<< Come on in. Just stoked the fire. Take a seat and get the cold out. >>"
        line3 = "<< Welcome. Let me know if you want anything... think I got a clean mug around here somewhere. >>"
        line4 = "<< Come on in. We got warm food, warm drinks, and warm beds. >>"
        choice_slogan = random.randint(1,4)
        if choice_slogan == 1:
            print(line1)
            pass
        elif choice_slogan == 2:
            print(line2)
            pass
        elif choice_slogan == 3:
            print(line3)
            pass
        elif choice_slogan == 4:
            print(line4)
            pass
        while True:
            if player.tavern_room_paid == False:
                user_input = input("> You may (T)alk, (B)uy or (S)ell. You may also rent a (R)oom for the night: it will cost you 30 Cash. Press (Q) to go away.>>\n>>>> ")
            else:
                user_input = input("<< You may (T)alk, (B)uy or (S)ell. Your room is upstairs. Press (Q) to quit.\n>>>> ")
            if user_input in ['Q', 'q']:
                print("<< See ya. >>\n")
                break
            elif user_input in ['b', 'B']:      # TODO ONLY CONSUMABLES here
                if self.talker.inventory != []:
                    print("****** Tavern Shop ******")
                    print("<< Drink for the thirsty, food for the hungry. >>")
                    player.trade(buyer=player, seller=self.talker)
                else:
                    print("<< I'm out of stock, please come back later. >>")
                    continue
            elif user_input in ['s', 'S']:
                if player.inventory != []:
                    print("<< What do you want to sell me, traveler? >>")
                    player.trade(buyer=self.talker, seller=player)
                else:
                    print("<< You don't have anything to sell. >>")
                    continue
            elif user_input in ['t', 'T', 'talk']:              # Info (vai al prossimo Q per le risposte)
                print("<< What do you want to know? >>\n")
                print("> 1 - What do you know about the Fattuzu?")
                print("> 2 - ")
                print("> 3 - I forgot my name. Can you tell me who am I?")
                print("> 4 - What do you know about an Intruder nearby?\n")

                user_input2 = input("> Choose a question or press Q go back.\n>>>> ")
                if user_input2 in ['1']:
                    print("<< Fattuzu is a mighty curse. They say is the worst curse of them all because it's casted by mushrooms: they're the smartest guys on Earth. >>\n")
                    continue
                elif user_input2 in ['2']:
                    print("<< >>\n")
                    continue
                elif user_input2 in ['3']:
                    print("<< It's obvious: you're {}. >>\n").format(player.name)
                    continue
                elif user_input2 in ['4']:
                    print("<< I've seen him down the river. He's not supposed to be there. But I guess that there's an Intruder inside all of us, after all... >>\n")
                    continue
                elif user_input2 in ['q', 'Q']:
                    print("<< What else do you need? >>")
                    continue
                else:
                    print("> I beg you pardon?")
                    continue

            elif user_input in ['r']:       # Affitti una stanza per la notte se hai abbastanza soldi
                if not player.tavern_room_paid:
                    if player.gold > 30:
                        cost = 30
                        player.gold = player.gold - cost
                        print(" << Thanks. Your room is to the north, upstairs. Let me know if there's anything else you need. >>")
                        print("> You now have {} Cash.".format(player.gold))
                        player.tavern_room_paid = True
                        continue
                    else:
                        print("<< What does this look like, the Temple of Mara? No gold, no bed. >>")
                        break
                else:
                    print("<< Are you joking? You just rented a room from me. >>")
            else:
                print("<< Try again. >>")
                continue

# |TR| *** TAVERN ROOM ***
class TavernRoomTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Tavern Room'
        self.talker = None
        self.enemy = None
        self.env_obj = []
        self.closed = False         # controlla chi è che si occupa di questa cosa
        self.description = "You are in a small room with wooden walls and floor. There is an uncomfortable looking bed on the west wall and a small desk on the east wall. The entrance door is to the south."
        self.examine = ""
        self.seen = False
        self.water = False
        super().__init__(x, y)

    def random_event(self, player):
        user_input = input("> You feel very tired, you better sleep now.\n>>>> ")
        if user_input in ['sleep', 'y', 'yes']:
            print("> *** RANDOM EVENT ***\n")
            print("> You go to sleep but something wakes you in the middle of the night.\n> As your eyes get used to the darkness you realize: it's a Random Event:\n")
            ananke = 3            # random.randint(0, 3)
            while True:
                if ananke == 0:
                    stolen_gold = random.randint(1, 50)
                    if player.gold >= stolen_gold:
                        player.gold = player.gold - stolen_gold
                        print(f">> A thief stole to you {stolen_gold} Cash and now you have {player.gold} remaining.\n")
                    else:
                        print(">> A thief tried to stole your Cash but you are too poor to be robbed.\n")
                elif ananke == 1:
                    gold = random.randint(1, 50)
                    player.gold = player.gold + gold
                    print(f">> The fairy give you {gold} Cash! You now have {player.gold}.\n")
                elif ananke == 2:
                    player.inventory.append(items.Ghirciola())
                    print(">> There's an item under your pillow.")
                    print(f">> It is a {items.Ghirciola()}! Taken.\n")
                else:
                    self.enemy = enemies.Thief()
                    print(">> Ambush!")
                    if player.base_defence > 0:
                        print("> You removed your armor for the night so you are more vulnerable.")
                        player.base_defence = 0
                    break
                self.seen = True
                print(f"\n\n\n> You stay the night at the Tavern and restore your health.\n>> You now have {player.gold} Cash and {player.hp} HP.\n")
                print("> (Time is passed: it's Tomorrow.)")
                player.tavern_room_paid = False
                player.hp = 100
                break
        elif user_input in ['no', 'q']:
            print("> As you wish. You shall sleep later.")
        else:
            print("> I beg you pardon?")

    def modify_player(self, player):
        super().modify_player(player)
        if self.enemy != None and not self.enemy.alive:
            print(f"> You sourvived this horrible night. You don't feel rested.\n>> You now have {player.gold} Cash and {player.hp} HP.\n")
            player.tavern_room_paid = False
            self.enemy = None
            return

# |TM| *** Temple ***
class TempleTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Temple'
        self.talker = npc.Monk()
        self.enemy = None
        self.description = "You are in a temple. Strange symbols made up of concentric circles adorn the walls. A monk prays in front of an altar filled with a liquid of a strange color."
        self.examine = None
        self.env_obj = []
        self.seen = False
        self.water = True
        super().__init__(x, y)

    def dialogue(self, player):
        line1 = "<< Give your bodies to Atom, my friends. Release yourself to his power, feel his Glow and be Divided. >>"
        line2 = "<< Come forth and drink the waters of the Glow, for this ancient weapon of war is our salvation, it is the very symbol of Atom's glory! >>"
        line3 = "<< Behold! He's coming with the clouds! And every eye shall be blind with his glory! Every ear shall be stricken deaf to hear the thunder of his voice! >>"
        line4 = "<< Yea, your suffering shall exist no longer; it shall be washed away in Atom's Glow, burned from you in the fire of his brilliance. >>"
        line5 = "<< Each of us shall give birth to a billion stars formed from the mass of our wretched and filthy bodies. >>"
        line6 = "<< Atom reached out and touched this world, bringing his Glow to us. It remains to this day, a reminder of his promise. Infinite worlds through divisions. >>"
        choice_slogan = random.randint(1,6)
        if choice_slogan == 1:
            print(line1)
        elif choice_slogan == 2:
            print(line2)
        elif choice_slogan == 3:
            print(line3)
        elif choice_slogan == 4:
            print(line4)
        elif choice_slogan == 5:
            print(line5)
        elif choice_slogan == 6:
            print(line6)
        while True:
            user_input = input("<< (B)uy, (S)ell or (Q)uit, child? I can also (H)eal you and Recharge your (M)ana, but every service will cost you 100 §. >>\n>>>> ").lower()
            if user_input in ['Q', 'q']:
                print("<< May you be Divided, child. >>\n")
                break
            elif user_input in ['b']:      # Only weapons
                if self.talker.inventory != []:
                    print("****** Monk ******")
                    print("<< Take a look. >>")
                    player.trade(buyer=player, seller=self.talker)
                else:
                    print("<< All sold. >>")
                    continue
            elif user_input in ['s']:
                if player.inventory != []:
                    print("<< What do you want to sell me, child? >>")
                    player.trade(buyer=self.talker, seller=player)
                else:
                    print("<< You don't have anything to sell. >>")
                    continue
            elif user_input in ['h']:
                if player.gold >= 100 and player.hp < player.max_hp:
                    player.hp = player.max_hp
                    player.gold -= 100
                    print("<< Thanks for your offer, child. All your wounds have been healed by the will of the Sacred Atom. >>")
                    continue
                elif player.hp == player.max_hp:
                    print("<< You are already in great shape, child. >>")
                    continue
                elif player.gold < 100:
                    print("<< Come back when you have more money, child. >>")
                    break
            elif user_input in ['m']:
                if player.gold >= 100 and player.mana < player.max_mana:
                    player.mana = player.max_mana
                    player.gold -= 100
                    print("<< Thanks for your offer, child. Your mana has been reloaded by the will of the Sacred Atom. >>")
                    continue
                elif player.mana == player.max_mana:
                    print("<< You are already in great shape, child. >>")
                    continue
                elif player.gold < 100:
                    print("<< Come back when you have more money, child. >>")
                    break
            else:
                print("<< Try again. >>")
                continue

# |WW| *** YOU WON ***
class VictoryTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Victory'
        self.talker = None
        self.enemy = None
        self.description = None
        self.examine = None
        self.seen = False
        self.env_obj = []
        self.water = False
        super().__init__(x, y)

    def modify_player(self, player):
        player.victory = True

    def intro_text(self):               # NOME della locazione corrente
        return """> The mistery is been revealed to ferns. Now they're happier and confused.

        Adesso comincia il secondo livello. Potrai scegliere di portare solo un numero limitato di oggetti
        con te, quelli che troverai nel secondo livello saranno completamente nuovi.

        You won.
        """

# |VS| *** VILLAGE SOUTH ***
class VillageSouthTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Village South'
        self.talker = None
        self.enemy = None
        self.description = "everything is collapsing ... over me, danger of going to the cemetery today."
        self.examine = None
        self.env_obj = []
        self.seen = False
        self.water = False
        super().__init__(x, y)

    def dialogue(self, player):
        print("everything is collapsing ... over me, danger of going to the cemetery today.")

# |VN| *** VILLAGE NORTH ***
class VillageNorthTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Village North'
        self.talker = None
        self.enemy = None
        self.description = None
        self.examine = None
        self.env_obj = []
        self.seen = False
        self.water = False
        super().__init__(x, y)


# >>>> FIGHT
# |X1|
class EnemyTile_1(MapTile):
    def __init__(self, x, y):
        self.name = 'ET1'
        self.talker = None
        self.enemy = None
        self.description = 'You are on a path surrounded by trees.'
        self.examine = None
        self.seen = False
        self.env_obj = []
        self.water = False
        r = random.randint(1, 4)
        if r == 1:
            self.enemy = enemies.GelCube()
        elif r == 2:
            self.enemy = enemies.NoMask()
        elif r == 3:
            self.enemy = enemies.Squirrel()
        else:
            self.enemy = enemies.Helicopter()
        super().__init__(x, y)

    # ok ho scoperto che è totalmente inutile!
    def modify_player(self, player):
        super().modify_player(player)

# |X2|
class EnemyTile_2(MapTile):
    def __init__(self, x, y):
        self.name = 'ET2'
        self.talker = None
        self.enemy = None
        self.description = 'You are on a path surrounded by trees.'
        self.examine = None
        self.seen = False
        self.env_obj = []
        self.water = False
        r = random.randint(1, 4)
        if r == 1:
            self.enemy = enemies.Cops()
        elif r == 2:
            self.enemy = enemies.MushroomHunter()
        elif r == 3:
            self.enemy = enemies.Incel()
        else:
            self.enemy = enemies.JacobChansley()
        super().__init__(x, y)

    def modify_player(self, player):
        super().modify_player(player)

# |X3|
class EnemyTile_3(MapTile):
    def __init__(self, x, y):
        self.name = 'ET3'
        self.talker = None
        self.enemy = None
        self.description = 'You are on a path surrounded by trees.'
        self.examine = None
        self.seen = False
        self.env_obj = []
        self.water = False
        r = random.randint(1, 4)
        if r == 1:
            self.enemy = enemies.Bug()
        elif r == 2:
            self.enemy = enemies.Eyes()
        elif r == 3:
            self.enemy = enemies.Ants()
        else:
            self.enemy = enemies.Trog()
        super().__init__(x, y)

    def modify_player(self, player):
        super().modify_player(player)

# |X4|
class EnemyTile_4(MapTile):
    def __init__(self, x, y):
        self.name = 'ET4'
        self.talker = None
        self.enemy = None
        self.description = 'You are on a path surrounded by trees.'
        self.examine = None
        self.seen = False
        self.env_obj = []
        self.water = False
        r = random.randint(1, 4)
        if r == 1:
            self.enemy = enemies.UncannyValley()
        elif r == 2:
            self.enemy = enemies.Paranoia()
        elif r == 3:
            self.enemy = enemies.Gnome()
        else:
            self.enemy = enemies.Mcu()
        super().__init__(x, y)

    def modify_player(self, player):
        super().modify_player(player)

# |X5|
class EnemyTile_5(MapTile):
    def __init__(self, x, y):
        self.name = 'ET5'
        self.talker = None
        self.enemy = None
        self.description = 'You are on a path surrounded by trees.'
        self.examine = None
        self.seen = False
        self.env_obj = []
        self.water = False
        r = random.randint(1, 4)
        if r == 1:
            self.enemy = enemies.Herobrine()
        elif r == 2:
            self.enemy = enemies.RubberJohnny()
        elif r == 3:
            self.enemy = enemies.ArmillariaOstoyae()
        else:
            self.enemy = enemies.MetaVerse()
        super().__init__(x, y)

    def modify_player(self, player):
        super().modify_player(player)

# >>>> WORLD
# ROW WORLD MAP
world_dsl = """
|  |  |  |  |  |  |TR|  |  |  |  |  |WW|
|  |  |  |  |  |  |TT|  |  |  |  |  |  |
|  |  |  |  |  |  |Lo|  |  |  |  |  |  |
|.4|.4|.4|.4|OK|FT|SS|.1|.1|.2|.2|.3|.3|
|.4|  |!!|  |.4|  |TM|  |.1|  |!!|  |.3|
|.5|  |!!|  |.5|  |BS|  |.1|  |!!|  |.3|
|.4|  |!!|  |.4|  |SQ|  |.1|  |!!|  |.3|
|.5|  |!!|  |.5|  |RC|  |.1|  |!!|  |.3|
|.5|.5|.5|.5|.5|.5|!!|.1|.1|.2|.2|.3|.3|

"""



"""
|  |  |  |  |TR|  |  |RV|IN|  |  |  |  |  |  |
|OK|  |  |  |TT|  |  |RV|  |  |  |Lo|  |  |  |
|  |.2|..|.2|..|.3|  |RV|  |.3|..|.3|..|.3|  |
|  |.2|  |.V|  |..|  |RV|  |..|  |  |  |.3|  |
|  |.1|  |Vn|  |.3|  |RV|  |.4|  |  |  |..|  |
|  |.2|  |Vs|  |.2|  |RV|  |..|  |  |  |.4|  |
|RC|..|  |BS|  |..|  |RV|  |.3|  |TR|  |..|  |
|  |.2|  |  |  |.3|.4|..|.3|.4|  |TT|  |.3|  |
|  |..|  |  |  |  |  |RV|  |  |  |..|  |..|  |
|  |.1|  |  |  |  |  |RV|  |  |  |.4|  |.4|  |
|  |.2|  |  |.1|.1|  |RV|  |  |  |..|  |.4|  |
|  |.1|..|..|.1|.1|  |RV|  |.5|..|..|.5|.4|  |
|  |  |.2|Lo|  |..|  |RV|  |..|  |Lo|  |  |  |
|  |  |.3|  |  |.1|  |RV|  |.5|  |  |  |  |  |
|  |.3|.2|  |FT|..|  |RV|..|..|  |  |  |  |  |
|  |  |.2|  |  |.2|  |RV|  |.5|  |.5|  |  |  |
|SS|..|.1|..|..|.1|  |RV|  |..|..|..|.5|.5|WW|
|  |  |.1|  |  |.1|  |RV|  |  |  |  |  |  |  |
"""


# Domain-Specific language
def is_dsl_valid(dsl):
    if dsl.count("|SS|") != 1:
        return False
    if dsl.count("|WW|") == 0:
        return False
    lines = dsl.splitlines()
    lines = [l for l in lines if l]
    pipe_counts = [line.count("|") for line in lines]
    for count in pipe_counts:
        if count != pipe_counts[0]:
            return False
    return True

tile_type_dict = {"BS": BlacksmithTile,
                  "!!": ChestTile,
                  ".1": EnemyTile_1,
                  ".2": EnemyTile_2,
                  ".3": EnemyTile_3,
                  ".4": EnemyTile_4,
                  ".5": EnemyTile_5,
                  "FT": FernsTile,
                  "IN": IntruderTile,
                  "Lo": Little_oTile,
                  "OK": OakTile,
                  "..": PathTile,
                  ".V": PathToVillageTile,
                  "RC": RinaTile,
                  "RV": RiverTile,
                  "SQ": SquareTile,
                  "SS": StartTile,
                  "SY": StyliteTile,
                  "TM": TempleTile,
                  "TT": TavernTile,
                  "TR": TavernRoomTile,
                  "WW": VictoryTile,
                  "Vn": VillageNorthTile,
                  "Vs": VillageSouthTile,
                  "  ": None}

world_map = []
start_tile_location = None

# WORLD CONSTRUCTION
def parse_world_dsl():
    if not is_dsl_valid(world_dsl):
        raise SyntaxError("DSL is invalid!")

    dsl_lines = world_dsl.splitlines()
    dsl_lines = [x for x in dsl_lines if x]

    for y, dsl_row in enumerate(dsl_lines):
        row = []
        dsl_cells = dsl_row.split("|")
        dsl_cells = [c for c in dsl_cells if c]
        for x, dsl_cell in enumerate(dsl_cells):
            tile_type = tile_type_dict[dsl_cell]
            if tile_type == StartTile:
                global start_tile_location
                start_tile_location = x, y
            row.append(tile_type(x, y) if tile_type else None)
        world_map.append(row)

def tile_at(x, y):
    if x < 0 or y < 0:
        return None
    try:
        return world_map[y][x]
    except IndexError:
        return None

def world_map_caller():
    return world_map