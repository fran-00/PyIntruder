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
        """Modify player and enemy based on a random chance of confusion
        and enemy's attack.
        
        Check if the enemy is alive and generate a random number to determine
        if the enemy becomes confused. Calculate damage reduction based on
        player's base defence and call damage_player().
        
        Parameters
        ----------
            player : Player
                The player to modify.

        Returns
        -------
            str
                A string describing the result of the enemy's attack.
            None
                If the enemy is dead or the attack misses.
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
        """Inflict damage to the player object based on enemy's attack and player's
        damage reduction.

        Parameters
        ----------
            player : Player
                The Player to be damaged.
            damage : int 
                The amount of damage to be inflicted on Player.
            damage_reduction : int or None
                The amount of damage reduction to be applied to the damage, or 
                None if no reduction is applied.

        Returns
        -------
            str
                A string describing the outcome of the attack.

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
            self.trade()
        elif args[1] == "talk":
            return
    
    def dialogue(self, *args):
        return "We are talking."
    
    def trade(self, *args):
        """Initiates a trade with an npc in the current room that wants to trade,
        if any.

        Parameters
        ----------
            *args (tuple)
                An optional tuple passed because play() method in GameModel
                class expects arguments to be passed.

        Returns
        -------
            str
                Prompt for the user to choose from the trade options.
            None
                If there is no npc in the current room or if npc doesn't want to trade.
        """
        if self.talker and self.talker.trade:
            sentence = self.talker.get_random_opening_sentence(f"{self.talker.name}")
            return f"{sentence}\nBuy, Sell or Quit?"
        elif self.talker and not self.talker.trade:
            return f"{self.talker.name} doesn't want to trade.", None
        else:
            return "There is no one to trade with.", None
    
    def look(self):
        """Show a detailed description of the current room's scenario.

        Returns
        -------
            str
                A detailed description of the current room and its features
        """
        response = self.description
        for item in self.inventory:
            response += f"\nThere is a {item.name} here."
        if self.talker:
            response += f"\nThere is {self.talker.name} here."
        if self.enemy and self.enemy.is_alive():
            response += f"\nThere is a {self.enemy.name} here, willing to kill you."
        if self.enemy and not self.enemy.is_alive():
            response += f"\nThere the corpse of a {self.enemy.name} here."
        return response