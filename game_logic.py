import os
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
