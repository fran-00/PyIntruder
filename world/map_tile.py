import random
from entities.factories.weapons_factory import WeaponsFactory as Wf
from entities.factories.curses_factory import CursesFactory as Cf
from entities.factories.armors_factory import ArmorsFactory as Af
from entities.factories.healers_factory import HealersFactory as Hf

# *** ROOM OF ROOMS ***
class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = []
        self.world_check = []
        self.random_items()

    def choose_random_items(self):
        n = random.randint(1, 4)
        if n in {1}:
            pass
        elif n in {2, 3}:
            self.inventory.extend(
                random.choice(Hf().get_items_list())
                for _ in range(random.randint(1, 2))
            )
        elif n == 4:
            self.inventory.append(random.choice(Wf().get_items_list()))

    def modify_player(self, player):
        """Modifies player and enemy based on a random chance of confusion and the enemy's attack.

        Args:
            player (Player): The player object to be modified.

        Returns:
            str or None: A string describing the result of the enemy's attack, or None if the enemy is dead or the attack misses.

        The function first checks if the enemy is alive and generate a random number to determine if the enemy becomes confused. 
        If the player has a base defence, the function calculates the damage reduction based on 5 times the player's base
        defence, and calls damage_player() with the calculated damage reduction.

        """
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
        """Inflicts damage to the player object based on the enemy's attack and the player's defense.

        Args:
            player (Player): The player object to be damaged.
            damage (int): The amount of damage to be inflicted on the player.
            damage_reduction (int or None): The amount of damage reduction to be applied to the damage, or None if no reduction is applied.

        Returns:
            str: A string describing the outcome of the attack.

        """
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


