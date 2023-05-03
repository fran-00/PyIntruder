import random, json

from entities.factories.weapons_factory import WeaponsFactory as Wf
from entities.factories.curses_factory import CursesFactory as Cf
from entities.factories.armors_factory import ArmorsFactory as Af
from entities.factories.healers_factory import HealersFactory as Hf


with open('world/data/tiles_data.json') as f:
    tiles_data = json.load(f)


# *** ROOM OF ROOMS ***
class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.description = tiles_data[f"{self.name}".lower()]["description"]
        self.inventory = []
        self.world_check = []
        self.choose_random_items()
        self.sort_inventory()

    def choose_random_items(self):
        healers_list = Hf().get_items_list()
        weapons_list = Wf().get_items_list()
        n = random.randint(1, 4)
        if n in {1}:
            pass
        elif n in {2, 3}:
            self.inventory.append(random.choice(healers_list))
        elif n == 4:
            self.inventory.append(random.choice(weapons_list))
    
    def sort_inventory(self):
        self.inventory.sort(key=lambda x: (x.__class__.__name__, x.name))
        return

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
        if self.enemy is None or not self.enemy.is_alive():
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

    def check_if_trading(self, *args):
        if args[1] == "trade":
            sentence = self.talker.get_random_opening_sentence(f"{self.talker.name}")
            return f"{sentence}\nBuy, Sell or Quit?"
        elif args[1] == "talk":
            return self.talker.hello
    
    def dialogue(self, *args):
        return "We are talking."