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
                return (f"> {self.room.enemy.intro_alive}")
            elif self.player.verbose and self.room.enemy.alive is False:
                return (f"\n***{self.room.name}***\n>{self.room.enemy.intro_dead}")
            elif not self.player.verbose and self.room.enemy is None:
                return (f"\n***{self.room.name}***")
    
            
    def choose_action(self, action=str):

        if action in ["diagnose"]:
            return(self.player.diagnose())


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