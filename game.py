from collections import OrderedDict
import os
import random
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot

import world
import items
from player import Player

class Game(QObject):
    model_signal_to_controller = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.play()
        self.output = None

    def play(self):
        world.parse_world_dsl()
        player = Player()
    #    player.name = input("> What's your name?\n")

        self.output = "\n***** THE MAJESTIC REPOSITIONING OF INTRUDERS *****\n"
        self.handle_outbound_signal(self.output)

        print("")
        print("> Not so freely inspired by several true stories.\n")
        print("> Ever since you learned about Fattuzu, you know you need to prevent The End Of The World As We Know It.")
        print("> In this game, melee weapons may fail while curses cannot, but they cost mana. During a fight the best weapon you have in your inventory is automatically selected, while you will have to choose which curse to cast, evaluating (in addition to the damage inflicted) also how much mana you have left to invest. Type 'diagnose' to know your health and mana.")
        print("> Anyway, you came from west. There's a path to the east.")
        while player.is_alive() and not player.victory:
            room = world.tile_at(player.x, player.y)

            if player.verbose and room.enemy is None:
                print(f"\n***{room.name}***")
                print(f"> {room.description}")
            elif (
                player.verbose
                and room.enemy.alive is True
                or not player.verbose
                and room.enemy is not None
                and room.enemy.alive is True
            ):
                print(f"> {room.enemy.intro_alive}")
            elif player.verbose and room.enemy.alive is False:
                print(f"\n***{room.name}***")
                print(f"> {room.enemy.intro_dead}")
            elif not player.verbose and room.enemy is None:
                print(f"\n***{room.name}***")

            player.turn += 1
            room.modify_player(player)

            if room.name in ["Tavern Room"] and room.enemy is None and player.tavern_room_paid is True:
                room.random_event(player)

            if player.is_alive() and not player.victory:
                self.choose_action(room, player)

            elif not player.is_alive():
                print("> Grim Reaper, what are you doing? Remember that sharks are coming!!!!")
                while True:
                    decision = input("> (R)estore or Re(S)tart or (Q)uit? \n> ").lower()
                    if decision == 'q':
                        return
                    elif decision == 'r':
                        if os.path.isfile('./saved_data.pkl'):
                            player.restore()
                        else:
                            print("> There is no file to restore from!")
                            continue
                    else:
                        self.play()

    def choose_action(self, room, player):
        action = None
        while not action:
            available_actions = self.get_available_actions(room, player)
            action_input = input(">>>> ")
            print("")
            action = available_actions.get(action_input)

            if action:
                action()
                return action

    # *** ARMOR ***
            elif action_input in ['armor']:
                player.armor()

    # *** DIAGNOSE ***
            elif action_input in ['diagnose']:
                player.diagnose()

    # *** DROP ***
            elif action_input in ['drop']:
                if player.inventory:
                    print("> You look inside your pockets:")
                    player.dpg(room, player)
                else:
                    print("> Your pockets are already empty.")

    # *** DROP ALL ***
            elif action_input in ['drop all']:
                if player.inventory:
                    player.drop_all_get_all(room, player)
                else:
                    print("> Your pockets are already empty.")

    # *** EMPTY BOTTLE ***
            elif action_input in ['empty bottle']:
                check_bottle = [item for item in player.inventory
                        if isinstance(item, items.Bottle)]
                if check_bottle:
                    if player.bottle_full:
                        player.bottle_full = False
                        print("> Your bottle is now empty.")
                    else:
                        print("> Your bottle is already empty.")
                else:
                    print("> You have no bottle with you.")

    # *** EXAMINE (GENERAL) *** TODO incorporalo a quello dopo
            elif action_input in ['examine all', 'observe']:
                if room.examine is not None:
                    print(f"> {room.examine}")
                else:
                    print("> CONCENTRATE ON THE ENEMY! Your own life is at stake!!")
                    return
                if room.enemy is None and room.inventory:                                # Stampa una lista di cose che ci sono per terra, se ce ne sono.
                    print("\n> P.S.: I know you love gathering things. There's something you can collect:")
                    for i, item in enumerate(room.inventory, 1):
                        print(f">>> {i}. It's {item.name}. Instructions say: {item.description}")
                    return True
                else:
                    pass

    # *** EXAMINE ***
            elif action_input in ['examine']:
                player.examine_item()

    # *** FILL BOTTLE ***
            elif action_input in ['fill bottle']:
                check_bottle = [item for item in player.inventory
                        if isinstance(item, items.Bottle)]
                if check_bottle:
                    if not player.bottle_full:
                        if room.water:
                            player.bottle_full = True
                            print("> Your bottle is now full.")
                        else:
                            print("> There is no water to fill the bottle with.")   
                    else:
                        print("> Your bottle is already full.")
                else:
                    print("> You have no bottle with you.")

    # *** FORBIDDEN DIRECTIONS ***
            elif (available_actions != ['n', 's', 'w', 'e', 'nw', 'ne', 'sw', 'se'] and
                action_input in ['n', 's', 'w', 'e', 'nw', 'ne', 'sw', 'se'] and
                room.enemy is not None and room.enemy.alive is True):
                print("> You cannot leave while an enemy attacks you!")
                return

            elif available_actions != 'n' and action_input in ['n']:
                if room.enemy is None or room.enemy.alive is False:
                    print("> You can't go north from here.")

            elif available_actions != 's' and action_input in ['s']:
                if room.enemy is None or room.enemy.alive is False:
                    print("> You can't go south from here.")

            elif available_actions != 'w' and action_input in ['w']:
                if room.enemy is None or room.enemy.alive is False:
                    print("> You can't go west from here.")

            elif available_actions != 'e' and action_input in ['e']:
                if room.enemy is None or room.enemy.alive is False:
                    print("> You can't go east from here.")

            elif available_actions != 'nw' and action_input in ['nw']:
                if room.enemy is None or room.enemy.alive is False:
                    print("> You can't go northwest from here.")

            elif available_actions != 'ne' and action_input in ['ne']:
                if room.enemy is None or room.enemy.alive is False:
                    print("> You can't go northeast from here.")

            elif available_actions != 'sw' and action_input in ['sw']:
                if room.enemy is None or room.enemy.alive is False:
                    print("> You can't go southwest from here.")

            elif available_actions != 'se' and action_input in ['se']:
                if room.enemy is None or room.enemy.alive is False:
                    print("> You can't go southeast from here.")

            elif available_actions != 'h' and action_input in ['h']:
                print("> Your health is already full.")

            elif available_actions != 'a' and action_input in ['a']:
                print("> There is no one to attack here.")

            elif available_actions != 'c' and action_input in ['c']:
                print("> There is no one to curse here.")

    # *** FORMER ROOM ***
            elif action_input in ['before']:
                print(f"> Former room is {player.previous_x}, {player.previous_y}")

    # *** GIVE ***
            elif action_input in ['give']:
                if player.inventory and room.talker:
                    print(f"> You look inside your pockets:")
                    player.dpg(room.talker, player)
                elif player.inventory and room.talker is None:
                    print("> There's no one to give your stuff.")
                else:
                    print("> You don't have anything to give.")

    # *** HELP ***
            elif action_input in ['help']:
                print(f"> Here are some commands you can try:")
                print(f"armor   Attack   brief   Cast curse   diagnose   drop   drop all")
                print(f"empty bottle   examine   fill bottle   give   Heal   Inventory")
                print(f"Look   Map   Open   self   Recharge Mana   roll   Run   pick up")
                print(f"Talk   verbose   ")
                print(f"> the first letter of the word is sufficient to enter the commands in uppercase.")

    # *** INVENTORY ***
            elif action_input in ['i', 'inventory']:
                if not player.inventory:
                    print("> Your inventory is empty.")
                elif room.enemy != None and room.enemy.alive is True:
                    print("> Fight! This is no time to rummage in your backpack!")
                    return
                else:
                    player.show_inventory()
                
    # *** LOOK ***
            elif action_input in ['l', 'look', 'see']:
                if room.enemy is None or room.enemy.alive is False:
                    game_output = f"> {room.description}\n"
                if room.enemy is not None and room.enemy.alive is True:
                    game_output = f"> {room.enemy.look_alive}"
                elif room.enemy is not None and room.enemy.alive is False:
                    game_output = f"> {room.enemy.look_dead}"
                if room.talker is not None:
                    game_output = f"> {room.talker.name} is here and looks at you."

    # *** MAP ***
            elif action_input in ['m', 'map']:
                if not room.enemy or not room.enemy.alive:
                    print(player.print_map())
                else:
                    print("> Do you really think it's time to consult a map? I don't think so.")
                    return

    # *** OPEN ***
            elif action_input in ['o', 'open', 'open it']:                                # Se c'è un qualcosa da aprire nella stanza, ti ci fa interagire se ancora non lo hai fatto.
                if room.env_obj:
                    player.open_obj()
                else:
                    print("> There's nothing to open here.")

    # *** PG DESCRIPTION ***
            elif action_input in ['self']:
                print(f"> Class : Warrior")
                print(f"> Name : {player.name}")
                print(f"> Level : {player.lvl}")
                print(f"> HP : {player.hp}/{player.max_hp}")
                print(f"> Mana : {player.mana}/{player.max_mana}")
                print(f"> § : {player.gold}")
                print(f"> XP : {player.xp}/{player.xp_modifier}")
                print(f"> Weapon equipped : {player.current_weapon}")
                print(f"> Turn : {player.turn}")
                print(f"> Location : {player.x}.{player.y}: {room.name}")           

    # *** RECHARGE MANA ***
            elif action_input in ['rm', 'recharge mana']:
                if player.mana < player.max_mana:
                    player.recharge_mana()
                    return
                else:
                    print("> Your mana is already full.")

    # *** ROLL ***
            elif action_input in ['roll']:
                if not room.enemy or not room.enemy.alive:
                    print("> You find a spot under a tree and sit on the ground to roll a joint...\n> Meanwhile an Ico is rolled too...")
                    d20 = random.randint(1, 20)
                    item = items.Modification()
                    if d20 == 1:
                        player.hp = player.hp - 20
                        print(f"> {d20}: You fail. And you also fall on a rock on the ground and lose health. You now have {player.hp} HP remaining.\n")
                    elif d20 in [ 2, 3, 4, 5 ]:
                        player.inventory.append(item)
                        print(f"> {d20} : You fail.\n")
                    elif d20 in [ 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 ]:
                        player.inventory.append(item)
                        print(f"> {d20}: Done.\n")
                    elif d20 in [ 16, 17, 18, 19 ]:
                        player.inventory.append(item)
                        player.inventory.append(item)
                        gold = random.randint(50, 100)
                        player.gold = player.gold + gold
                        print(f"> {d20}: You're already high, but still you manage to roll two joints instead of one. You find {gold} Pine Cones too.\n")
                    elif d20 == 20:
                        gold = random.randint(100, 200)
                        player.gold = player.gold + gold
                        player.inventory.append(item)
                        player.inventory.append(item)
                        player.inventory.append(item)
                        print(f"> {d20}: You're the king of ghirciola. Here's 3 to you and {gold} Pine Cones.\n")
                else:
                    print("> You can't roll during a battle!")
                    return

    # *** PICK UP ***
            elif action_input in ['pick up']:
                if room.inventory:
                    print("> Here's what you can collect:")
                    player.dpg(player, room)
                else:
                    print("> There's nothing to pick up.")

    # *** PICK UP ALL ***
            elif action_input in ['pick up all', 'get all']:
                if room.inventory:
                    player.drop_all_get_all(player, room)
                else:
                    print("> There's nothing to pick up.")

    # *** RESTORE ***
            elif action_input in ['restore']:
                player.restore()
                return
    # *** SAVE ***
            elif action_input in ['save']:
                player.save()
                print("> Your progress has been saved.")

    # *** TALK ***
            elif action_input in ['t', 'talk', 'speak']:
                if room.enemy is not None:
                    if room.enemy.alive is True:
                        print("> {}\n".format(room.enemy.talk_alive))
                        return
                    elif room.enemy.alive is False:
                        print("> {}\n".format(room.enemy.talk_dead))
                elif room.talker:
                    player.check_dialogue()
                else:
                    print("> Hmmm ... A tree looks at you expectantly, as if you seemed to be about to talk.")

    # *** VERBOSITY ***
            elif action_input in ['verbose']:
                player.verbose = True
                print("> Maximum verbosity.")
            elif action_input in ['brief']:
                player.verbose = False
                print("> Minimum verbosity.")

    # LAST *** UNRECOGNISED COMMAND *** fortunatamente se si sbaglia in questo modo il turno non viene contato, ma non capisco perché
            else:
                print("> I beg you pardon?")

    def handle_outbound_signal(self, output):
        ''' Takes a string an send it to controller as a signal '''
        print("I'm MODEL and I'm sending a signal to CONTROLLER!")
        print(f"The signal says: {output}")
        self.model_signal_to_controller.emit(output)

    # CHIAMA SOLO FUNZIONI
    def get_available_actions(self, room, player):
        actions = OrderedDict()

        if room.enemy is None or room.enemy.alive is False:
            self.available_directions(room, actions, player)
        if room.enemy is not None and room.enemy.alive is True:
            self.action_adder(actions, 'a', player.attack, "attack")
    #       print("\n| A = attack | H = heal |\n| C = spell  | R = run  |\n")
        if room.enemy is not None and room.enemy.alive is True:
            self.action_adder(actions, 'c', player.cast_curse, "cast curse")
        if room.enemy is not None and room.enemy.alive is True:
            self.action_adder(actions, 'r', player.run, "run")
        if room.talker:
            self.action_adder(actions, 't', player.check_dialogue, "talk")
        if player.hp < player.max_hp:
            self.action_adder(actions, 'h', player.heal, "heal")
        return actions


    def available_directions(self, room, actions, player):
        if world.tile_at(room.x, room.y - 1) and room.name not in ['Tavern']:
            self.action_adder(actions, 'n', player.move_north, "north")
        if world.tile_at(room.x, room.y - 1) and room.name in ['Tavern']:
            if player.tavern_room_paid is False:
                self.action_adder(actions, 'n', player.tavern_room_closed, "north")
            else:
                self.action_adder(actions, 'n', player.move_north, "north")
        if world.tile_at(room.x, room.y + 1):
            self.action_adder(actions, 's', player.move_south, "south")
        if world.tile_at(room.x + 1, room.y):
            self.action_adder(actions, 'e', player.move_east, "east")
        if world.tile_at(room.x - 1, room.y):
            self.action_adder(actions, 'w', player.move_west, "west")
        if world.tile_at(room.x - 1, room.y - 1):
            self.action_adder(actions, 'nw', player.move_northwest, "northwest")
        if world.tile_at(room.x + 1, room.y - 1):
            self.action_adder(actions, 'ne', player.move_northeast, "northeast")
        if world.tile_at(room.x - 1, room.y + 1):
            self.action_adder(actions, 'sw', player.move_southwest, "southwest")
        if world.tile_at(room.x + 1, room.y + 1):
            self.action_adder(actions, 'se', player.move_southeast, "southeast")

    def action_adder(self, action_dict, hotkey, action, name):
        action_dict[hotkey.lower()] = action
        action_dict[hotkey.upper()] = action
        print(f"| {hotkey}: {name}")