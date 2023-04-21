import os
from collections import OrderedDict

import world
from player import Player


class GameLogic:
    def __init__(self):
        self.player = Player()
        self.room = world.tile_at(self.player.x, self.player.y)
        
    def check_tile(self):
        if self.player.is_alive():

            if self.player.verbose and self.room.enemy is None:
                return (f"\n***{self.room.name}***\n>{self.room.description}")
            
            elif (
                self.player.verbose
                and self.room.enemy.alive is True
                or not self.player.verbose
                and self.room.enemy is not None
                and self.room.enemy.alive is True
            ):
                return (f"{self.room.enemy.intro_alive}")
            elif self.player.verbose and self.room.enemy.alive is False:
                return (f"\n***{self.room.name}***\n>{self.room.enemy.intro_dead}")
            elif not self.player.verbose and self.room.enemy is None:
                return (f"\n***{self.room.name}***")
    
            
    def choose_action(self, action=str):
        available_actions = self.get_available_actions(self.room, self.player)
        # FIXME:
        # action = available_actions.get(action)

        if action in ["diagnose"]:
            return(self.player.diagnose())
        
        elif action in ['before']:
                return (f"Former room is {self.player.previous_x}, {self.player.previous_y}")

        # *** FORBIDDEN DIRECTIONS ***
        elif (available_actions != ['n', 's', 'w', 'e'] and
            action in ['n', 's', 'w', 'e'] and
            self.room.enemy is not None and self.room.enemy.alive is True):
            return ("You cannot leave while an enemy attacks you!")

        elif available_actions != 'n' and action in ['n']:
            if self.room.enemy is None or self.room.enemy.alive is False:
                return ("You can't go north from here.")

        elif available_actions != 's' and action in ['s']:
            if self.room.enemy is None or self.room.enemy.alive is False:
                return ("You can't go south from here.")

        elif available_actions != 'w' and action in ['w']:
            if self.room.enemy is None or self.room.enemy.alive is False:
                return ("You can't go west from here.")

        elif available_actions != 'e' and action in ['e']:
            if self.room.enemy is None or self.room.enemy.alive is False:
                return ("You can't go east from here.")

        elif available_actions != 'h' and action in ['h']:
            return ("Your health is already full.")

        elif available_actions != 'a' and action in ['a']:
            return ("There is no one to attack here.")

        elif available_actions != 'c' and action in ['c']:
            return ("There is no one to curse here.")

        else:
            return("I beg you pardon?")


    def get_available_actions(self, room, player):
        actions = OrderedDict()

        if room.enemy is None or room.enemy.alive is False:
            self.available_directions(room, actions, player)
        if room.enemy is not None and room.enemy.alive is True:
            self.action_adder(actions, 'a', player.attack, "attack")
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


