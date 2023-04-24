import random

import old_entities_data.enemies as enemies
import old_entities_data.npc as npc
from entities.player import Player
import old_entities_data.items as items
from entities import entities_index
import old_entities_data.environmental_objects as environmental_objects


# *** ROOM OF ROOMS ***
class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = []
        self.world_check = []


    def random_item(self):
        n = random.randint(1, 4)
        if n in {1, 2}:
            pass
        elif n == 3:
            self.inventory.extend(
                random.choice(entities_index.consumables_list)
                for _ in range(random.randint(1, 2))
            )
        elif n == 4:
            self.inventory.append(random.choice(entities_index.mrs_list))


    def modify_player(self, player):
        if self.enemy is not None and self.enemy.alive is True:
            confusion_chance = random.randint(1, 20)
            if confusion_chance >= 19 and self.enemy.damage < self.enemy.hp:                       #in questo modo non può uccidersi da solo
                self.enemy.hp -= self.enemy.damage
                return (f"{self.enemy.name} is confused!\nIt hurts itself in its confusion! (Deals {self.enemy.damage} DMG and has {self.enemy.hp} HP remaining.)")
            elif confusion_chance in [17, 18]:
                return (f"{self.enemy.name} is confused!\n{self.enemy.name} misses the shot!")
            elif player.base_defence == 0:
                player.hp = player.hp - self.enemy.damage
                if player.hp > 0:
                    return (f"{self.enemy.name} inflicts {self.enemy.damage} DMG to you. Oh shit, you have {player.hp} HP remaining...")
                elif player.hp <= 0:
                    return (f"{self.enemy.name} inflicts {self.enemy.damage} DMG to you. Oh shit, you died...")
            elif player.base_defence > 0:
                damage_reduction = 5 * player.base_defence
                if damage_reduction < self.enemy.damage:
                    player.hp = player.hp - (self.enemy.damage - damage_reduction)
                    if player.hp > 0:
                        return (f"{self.enemy.name} inflicts {self.enemy.damage} DMG to you, but your armor reduce the damage by {damage_reduction}, so you have {player.hp} HP remaining...")
                    elif player.hp <= 0:
                        return (f"{self.enemy.name} inflicts {self.enemy.damage} DMG to you, your armor reduce the damage by {damage_reduction} but you died anyway...")
                else:
                    return (f"{self.enemy.name} tries to inflict {self.enemy.damage} DMG to you, but your armor absorbes {damage_reduction} DMG, so it did nothing to you and you still have {player.hp} HP remaining...")
        else:
            return


