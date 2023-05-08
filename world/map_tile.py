import random, json, re

from entities.factories import healers, weapons


with open('world/data/tiles_data.json') as f:
    tiles_data = json.load(f)

with open('entities/data/npcs_data.json') as nf:
    npcs_data = json.load(nf)


# *** ROOM OF ROOMS ***
class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.description = tiles_data[f"{self.name}".lower()]["description"]
        self.inventory = []
        self.environment = []
        self.enemy = None
        self.talker = None

        self.choose_random_items()
        self.sort_inventory()

    def choose_random_items(self):
        healers_list = healers().get_items_list()
        weapons_list = weapons().get_items_list()
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

    def choose_talking_npc(self, *args):
        target = args[2]
        if self.talker.name.lower() == target:
            response = ""
            opening_sentece = npcs_data[self.talker.name.lower()]['opening sentence']
            response += f"{opening_sentece}"
            player_dialogue = npcs_data[self.talker.name.lower()]['player dialogue 0']
            for i, sentence in enumerate(list(player_dialogue.values())):
                response += f"\n{i}: {sentence}"
            return response
        elif self.enemy:
            # TODO: add enemy dialogues
            return "Enemy talks", None
        elif not self.talker and not self.enemy:
            return "Hmmm ... A tree looks at you expectantly, as if you seemed to be about to talk.", None

    def dialogue(self, *args):
        # TODO: Parse dialogues from npc dialogue 0
        return
    
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
        print(self.environment)
        for surrounding in self.environment:
            response += f"\nThere is a {surrounding} here."
        if self.talker:
            response += f"\nThere is {self.talker.name} here."

        if self.enemy and self.enemy.is_alive():
            response += f"\nThere is a {self.enemy.name} here, willing to kill you."
        elif self.enemy and not self.enemy.is_alive():
            response += f"\nThere the corpse of a {self.enemy.name} here."
        return response
    
    def look_at(self, target, player):
        """Return the description of the object or item with the given target name in the room.
        
        Parameters
        ----------
        target: str
            The name of the object or item to look at.
        player: Player
            The Player class to examine items in inventory
        
        Returns
        -------
        str
            The description of the target object or item, or a message 
            if no matching target is found.
        """
        objects_to_check = [self, self.talker, self.enemy] + self.inventory + self.environment + player.inventory
        for obj in objects_to_check:
            if obj and re.search(rf"\b\w*({''.join([f'{c}' for c in target])})\w*\b", obj.name.lower()):
                return obj.description
        return(f"I can't see any {target} here.")

    def open(self, target):
        """_summary_

        Parameters
        ---------
            target : str
                _description_
        """
        for object in self.environment:
            if target == object.name.lower():
                if object.openable:
                    return f"You open {object.name}"
                else:
                    return f"You cannot open it."
            else:
                return "I beg your pardon?"
        else:
            return "There is nothing to open here."