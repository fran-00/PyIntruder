import random
from dataclasses import dataclass

from entities.templates import Weapon
import world.parser as parser
from styles.decorators import *


@dataclass
class Combat:

    @staticmethod
    def best_weapon(inventory):
        """Find the best weapon in an inventory and return it.

        Returns
        -------
        best_weapon : Weapon
            The weapon in the player's inventory with higher damage attribute
        None
            The player has no weapons.
        """
        max_damage = 0
        best_weapon = None
        if weapons := [
            item for item in inventory if isinstance(item, Weapon)
        ]:
            for _, item in enumerate(weapons, 1):
                if item.damage > max_damage:
                    best_weapon = item
                    max_damage = item.damage
            return best_weapon
        else:
            return None

    @staticmethod
    def attack_command_handler(player):
        """Attempt to attack an enemy in the current room with the best
        available weapon.

        Returns
        -------
        str
            Return the result of calling calculate_attack_precision() with
            arguments for the enemy, weapon, and a message about the attack
            attempt.
            If the player has no weapon, return a message stating this.
        None
            If there is no living enemy in the room, return None.
        """
        weapon = Combat.best_weapon(player.inventory)
        room = parser.tile_at(player.x, player.y)
        enemy = room.enemy
        response = ""

        if weapon is None:
            return "You don't have any weapon with you."

        if enemy is None or not enemy.is_alive():
            return

        response += f"<p>You try to hit {enemy.styled_name()} with {weapon.name}!</p>"
        return Combat.calculate_attack_precision(player, enemy, weapon, response)

    @staticmethod
    def curse_command_handler(player, enemy, choice):
        """Cast a curse on an enemy.

        Called by show_appropriate_answer() method if purpose argument is
        "Curse". If there is not enough mana to cast the spell, return a string
        indicating so. Otherwise, subtract the mana cost from the caster's mana
        pool and the curse's damage from the target's hp.

        Parameters
        ----------
        enemy : Enemy
            The enemy in the current room.
        choice : Curse
            The choosen curse returned by choose_item() method.

        Returns
        -------
        str
            Return a formatted string indicating name of the spell cast,
            damage dealt and remaining mana.
        """
        if choice.mana_cost > player.mana:
            return f"You don't have enough mana to cast {choice.name}!"
        response = ""
        d20 = random.randint(1, 20)
        if d20 in {19, 20}:
            enemy.hp -= choice.damage * 2
            response += (
                f"<p>Critical hit!</p>"
                f"<p>You cast {choice.name} on {enemy.styled_name()}.</p>"
                f"<p>It does {choice.damage*2} DMG!</p>"
            )
        else:
            enemy.hp -= choice.damage
            response = (
                f"<p>You cast {choice.name} on {enemy.styled_name()}.</p>"
                f"<p>It does {choice.damage} DMG!"
            )
        player.mana -= choice.mana_cost
        response += f"<p>You now have {player.mana} Mana remaining.</p>"
        return response

    @green_text
    @staticmethod
    def calculate_attack_precision(player, enemy, weapon, response):
        """Calculate attack precision and damage multiplier based on a random integer.

        Parameters
        ----------
        enemy : Enemy
            An Enemy class instance alive in the current room.
        weapon : Weapon
            Best player's weapon, if any.
        response : str
            A string to add to the response.

        Returns
        -------
        func
            Call check_enemy_hp() passing enemy and response string as arguments
        """
        precision = random.randint(1, 20)
        match precision:
            case 20:
                damage_multiplier = 2
                response += (
                    f"<p>Critical hit!</p>"
                    f"<p>You deal {weapon.damage * damage_multiplier} DMG!</p>"
                )
            case 17 | 18 | 19:
                damage_multiplier = 1.5
                response += (
                    f"<p>Good hit!</p>"
                    f"<p>You deal {weapon.damage * damage_multiplier} DMG!</p>"
                )
            case 3 | 2 | 1:
                response += "<p>Missed!</p>"
                return response
            case _:
                damage_multiplier = 1
                response += f"<p>You deal {weapon.damage} DMG!</p>"

        enemy.hp -= weapon.damage * damage_multiplier
        return Combat.check_enemy_hp(player, enemy, response)

    @green_text
    @staticmethod
    def check_enemy_hp(player, enemy, response):
        """Check the HP of an enemy and responds accordingly.

        Parameters
        ----------
        enemy : Enemy
            An instance of Enemy class representing the enemy being checked.
        response : str
            The current response string that is being built.

        Returns
        -------
        str
            The updated response string after checking the enemy's HP.
        """
        if not enemy.is_alive():
            response += "<p>YEAH! You killed it!</p>"
            response += Combat.calculate_xp_earned(player, enemy)
            loot = random.randint(10, 200)
            player.gold += loot
            response += f"<p>{enemy.styled_name()} lost his booty. Now {loot} § are yours!</p>"

        else:
            response += f"<p>{enemy.styled_name()} has {enemy.hp} HP remaining.</p>"
        return response

    @staticmethod
    def calculate_xp_earned(player, enemy):
        """Calculate the earned XP points from killing an enemy, update Player
        level if necessary and return the response string for the XP gain.

        Parameters
        ----------
        enemy : Enemy
            An instance of Enemy class representing killed enemy.

        Returns
        -------
        str
            The updated response string after earning XP.
        """
        xp_earned = (enemy.damage)  # TODO: create a way to calculate XP
        response = f"<p>You earned {xp_earned} XP!</p>"
        player.xp += xp_earned
        if player.xp >= player.xp_modifier:
            response += player.level_up()
        return response
