import random

from entities.factories.npcs_factory import NPCsFactory as NPCf
from entities.factories.weapons_factory import WeaponsFactory as Wf
from entities.factories.armors_factory import ArmorsFactory as Af
from entities.factories.healers_factory import HealersFactory as Hf
from entities.factories.quest_items_factory import QuestItemsFatory as QIf
from entities.factories.enemies_factory import EnemiesFactory as Ef
from world.map_tile import MapTile


# |SS| *** Start ***
class StartTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Clearing'
        self.enemy = None
        self.talker = None
        self.description = "You are in a clearing. You arrived with your car from the west and the road ends in the east, where a path that climbs the mountain begins. A dense network of trees prevents the passage in any other direction. Your car is parked on the north side of the clearing, there is no one else parked."
        self.examine = "Your car is warm. Outside is cold."
        self.water = True
        super().__init__(x, y)
        # in this way the inventory inherit from parent class gets overidden
        self.inventory = [Wf().sheet]

    def room_seen(self):
        self.seen = True

# |Lo| *** Little(o) ***
class Little_oTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Little(o)'
        self.talker = NPCf().littleo
        self.enemy = None
        self.description = "They say it is only infinitesimally probable to be here."
        self.examine = "It's an experimental application of Infinite Improbability, which in the future will led to the Infinite Improbability Drive."
        self.water = False
        super().__init__(x, y)

    def dialogue(self, player):
        print("<< Little(o)! >>")
        while True:
            choice_slogan = random.randint(1,9)
                
            user_input = input("<< You are at Little(o)! (B)uy, (S)ell or (Q)uit? >>\n>>>> ")
            if user_input in ['Q', 'q']:
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

# |BS| *** Blacksmith ***
class BlacksmithTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Blacksmith'
        self.talker = NPCf().blacksmith
        self.enemy = None
        self.description = "You are in a blacksmith's shop. He is working on an anvil by striking a hot iron with a hammer. The room is small, full of tools, and it's hot as hell."
        self.water = True
        super().__init__(x, y)

    def dialogue(self, player):
        choice_slogan = random.randint(1,6)
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
        self.env_obj = None
        self.description = "There's a chest here.\n"
        self.examine = "Chest has a Icosahedron on it."
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
                        self.enemy = Ef.Lv1().helicopter
                        self.closed = False
                        print(f"{self.enemy.intro_alive}")
                    elif ico == 0:                       # se esce 0
                        print(f"> {ico}! Hard Enemy!")
                        self.enemy = Ef.Lv1().gel_cube()
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
        self.talker = NPCf().ferns
        self.enemy = None
        self.description = "A lot of ferns."
        self.examine = "They're green and worried."
        self.inventory = [Hf().ats]
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
                    player.inventory.append(QIf().specimen)
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
        self.water = False
        super().__init__(x, y)

# |IN| *** Intruder ***
class IntruderTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Down the river'
        self.talker = NPCf.Intruder()
        self.enemy = None
        self.description = "It shouldn't be here"
        self.examine = "It shouldn't be here"
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

# |OK| *** Oak ***
class OakTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Oak'
        self.enemy = None
        self.talker = NPCf().oak
        self.description = "There's n Oak here."
        self.examine = "OMG he's very wise."
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
        if randomguy is NPCf().prolonged:                      # FIXME non riesco a fargli scegliere quale dialogo far partire
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
        self.water = False
        super().__init__(x, y)

# |Rn| *** Rina Casti ***
class RinaTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Rina Casti'
        self.enemy = None
        self.talker = NPCf().rina
        self.description = "You're surrounded by trees. There's someone here."
        self.examine = " "
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
            player.inventory.append(Af().rinas_armor)
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
        self.water = True
        super().__init__(x, y)

# |SQ| *** Square ***
class SquareTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Little Square'
        self.talker = NPCf().merchant
        self.enemy = None
        self.description = "You are in a square, deserted except for a slimy-looking merchant behind a stall full of all kinds of equipment. In the center of the square is a fountain with a statue of a familiar-looking plant in the center."
        self.water = True
        super().__init__(x, y)

    def dialogue(self, player):
        choice_slogan = random.randint(1,6)
        print("> You approach the stall to ask the merchant to show you his wares.")
        
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

# |Sy| *** STYLITE ***
class StyliteTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Stylite'
        self.enemy = None
        self.talker = NPCf().stylite
        self.description = "There is a kind of cross in the trees, it is tall and there is a man in his underwear on it"
        self.examine = ""
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
        self.talker = NPCf().innkeeper
        self.enemy = None
        self.description = "You are in a tavern. The whole structure is dark wood, there are a dozen round tables but no people but you and the tavern keeper. He is behind the counter cleaning glasses and greets you with a smile and a nod of his head. The counter is to the right of the entrance and there are stairs to the north that lead to the upper floor, which houses the rooms for the overnight stay."
        self.examine = " Mah."
        self.water = True
        super().__init__(x, y)

    def dialogue(self, player):
        choice_slogan = random.randint(1,4)
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
        self.closed = False         # controlla chi è che si occupa di questa cosa
        self.description = "You are in a small room with wooden walls and floor. There is an uncomfortable looking bed on the west wall and a small desk on the east wall. The entrance door is to the south."
        self.examine = ""
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
                    player.inventory.append(Hf.ats)
                    print(">> There's an item under your pillow.")
                    print(f">> It is a {Hf().ats}! Taken.\n")
                else:
                    self.enemy = Ef.Lv1().gel_cube
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
        self.talker = NPCf().monk
        self.enemy = None
        self.description = "You are in a temple. Strange symbols made up of concentric circles adorn the walls. A monk prays in front of an altar filled with a liquid of a strange color."
        self.water = True
        super().__init__(x, y)

    def dialogue(self, player):
        choice_slogan = random.randint(1,6)  
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
        self.water = False
        super().__init__(x, y)

