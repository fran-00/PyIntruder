import random

from entities import entities_index


# *** ROOM OF ROOMS ***
class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = []
        self.world_check = []
        
        self.random_item()

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
        if self.enemy is None or not self.enemy.alive:
            return
        confusion_chance = random.randint(1, 20)
        if confusion_chance >= 19 and self.enemy.damage < self.enemy.hp:
            self.enemy.hp -= self.enemy.damage
            return (
                f"{self.enemy.name} is confused!\n"
                f"It hurts itself in its confusion! "
                f"(Deals {self.enemy.damage} DMG and has {self.enemy.hp} HP remaining.)"
            )

        if confusion_chance in [17, 18]:
            return f"{self.enemy.name} is confused!\n{self.enemy.name} misses the shot!"
        if player.base_defence == 0:
            return self.damage_player(player, self.enemy.damage, None)
        damage_reduction = 5 * player.base_defence
        return self.damage_player(player, self.enemy.damage, damage_reduction)

    def damage_player(self, player, damage, damage_reduction):
        if damage_reduction is not None:
            damage -= damage_reduction

        player.hp -= damage

        if player.hp <= 0:
            return (
                f"{self.enemy.name} inflicts {damage} DMG to you, "
                f"your armor reduce the damage by {damage_reduction or 0} but you died anyway..."
            )
        if damage_reduction is not None:
            return (
                f"{self.enemy.name} inflicts {damage} DMG to you, "
                f"but your armor reduce the damage by {damage_reduction}, "
                f"so you have {player.hp} HP remaining..."
            )
        return (
            f"{self.enemy.name} inflicts {damage} DMG to you. "
            f"Oh shit, you have {player.hp} HP remaining..."
        )


