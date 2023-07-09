import random
import json
import re

from entities.templates import Healer, ManaRecharger, Trader
from entities.factory import ItemsFactory as items


with open('world/data/tiles_data.json') as f:
    tiles_data = json.load(f)

with open('entities/data/npcs_data.json') as nf:
    npcs_data = json.load(nf)

with open('entities/data/enemies_data.json') as ef:
    enemies_data = json.load(ef)


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
        self.water = False
        self.choose_random_items()

    def handle_event(self, *args):
        pass

    def choose_random_items(self):
        """Choose one or two random items from either the Healer or ManaRecharger
        entities lists and add them to room's inventory.
        """
        healers_list = items().get_entities_list(Healer)
        manarechargers_list = items().get_entities_list(ManaRecharger)
        n = random.randint(1, 4)
        if n in {1}:
            pass
        elif n in {2, 3}:
            self.inventory.append(random.choice(healers_list))
        elif n == 4:
            self.inventory.append(random.choice(manarechargers_list))

    # -------------------------------------------------------------------------|
    # COMBAT ------------------------------------------------------------------|
    # -------------------------------------------------------------------------|

    def modify_player(self, player):
        """Modify player and enemy based on a random chance of confusion
        and enemy's attack.

        Check if the enemy is alive and generate a random number to determine
        if the enemy becomes confused. Calculate damage reduction based on
        player's base defence and call calculate_damage().

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

        if confusion_chance in {17, 18}:
            return f"{self.enemy.name} is confused!\n{self.enemy.name} misses the shot!"
        if player.base_defence == 0:
            return self.calculate_damage(player, self.enemy.damage, None)
        damage_reduction = 5 * player.base_defence
        return self.calculate_damage(player, self.enemy.damage, damage_reduction)

    def calculate_damage(self, player, damage, damage_reduction):
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

    # -------------------------------------------------------------------------|
    # DIALOGUES ---------------------------------------------------------------|
    # -------------------------------------------------------------------------|

    def choose_talking_npc(self, *args):
        """Choose which NPC to talk to based on target and on which entities
        are in the current room.

        Parameters
        ----------
        *args
            A tuple that contains two arguments:
            *args[0]: The Player class
                Is passed as an argument to call match_target_name() method.
            *args[1]: The target
                String representing who the player wants to talk to.

        Returns
        -------
        tuple : (str, None)
            A specific dialogue string in case of merchant or enemy and None
            value to break model's game loop.
        tuple : (str, str, int, int)
            If the player is talking to an npc that has nested dialogs, provide
            arguments to pass to dialogue() method and enter dialogue loop.
        """
        player = args[0]
        target = args[1]
        response = ""
        if self.talker and player.match_target_name(target, self.talker):
            return self.dialogue_starter(response)
        elif self.enemy and player.match_target_name(target, self.enemy):
            if self.enemy.is_alive():
                response = enemies_data[self.enemy.name.lower()]['talk_alive']
            else:
                response = enemies_data[self.enemy.name.lower()]['talk_dead']
            return response, None
        else:
            response = "Hmmm ... A tree looks at you expectantly, as if you seemed to be about to talk."
            return response, None

    def dialogue_starter(self, response):
        response += self.talker.get_random_opening_sentence(f"{self.talker.name}")
        if isinstance(self.talker, Trader):
            return response, None
        player_dialogue = npcs_data[self.talker.name.lower()]['dialogues']['player 0']
        for current_dialogue, sentence in enumerate(list(player_dialogue.values())):
            response += f"\n{current_dialogue + 1}: {sentence}"
        number_of_dialogues = len(npcs_data[self.talker.name.lower()]['dialogues'])
        return response, "dialogue", current_dialogue, number_of_dialogues

    def dialogue(self, *args):
        """Show NPC and player dialogues based on the current dialogue count,
        total number of dialogues and player's choice.

        Parameters
        ----------
        *args (any):
            A tuple that contains five arguments:
            *args[0]: Player (class)
                The player class, passed as an argument due to how model's
                process_nested_loop method works, is used by choose_talking_npc()
                to call match_target_name()
            *args[1]: target (str)
                String representing who the player wants to talk to, is used
                by choose_talking_npc()
            *args[2]: current_dialogue (int)
                Integer representing the current dialogue number.
            *args[3]: number_of_dialogues (int)
                An integer representing the total number of dialogues.
            *args[4]: choice (str)
                String representing the player's dialogue choice which must be
                converted to int type.

        Returns
        -------
        tuple : (str, str, int, int)
            If current_dialogue < number_of_dialogues, provide
            arguments to pass to the next dialogue() method call.
        tuple : (str, None)
            If the player exits the dialogue, return a tuple with a message as
            first argument and None as second argument to break game loop.
        tuple : (None, None)
            If dialogues are over return a tuple None as second argument to
            break game loop.

        Raises
        ------
        Exception
            In case of invalid player choice, raise an exception with an error message.
        """
        number_of_dialogues = args[-2]
        current_dialogue = args[-3]
        if number_of_dialogues == current_dialogue:
            return None, None
        choice = args[-1]
        if choice.lower() in ["quit", "q", "exit"]:
            return "Action cancelled.", None
        npc_dialogues = list(npcs_data[self.talker.name.lower()]['dialogues'][f'npc {current_dialogue}'].values())
        player_dialogue = list(npcs_data[self.talker.name.lower()]['dialogues'][f'player {current_dialogue}'].values())
        response = ""
        try:
            choice_index = int(choice)
            sentence = npc_dialogues[choice_index - 1]
            response += f"{sentence}"
            for i, sentence in enumerate(player_dialogue):
                response += f"\n{i + 1}: {sentence}"
            current_dialogue += 1
            number_of_dialogues -= 1
            return response, "dialogue", current_dialogue, number_of_dialogues
        except Exception as e:
            return f"{e}"

    # -------------------------------------------------------------------------|
    # TRADING -----------------------------------------------------------------|
    # -------------------------------------------------------------------------|

    def trade(self, *args):
        """Initiate a trade with an npc in the current room that wants to trade,
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
        if self.talker and isinstance(self.talker, Trader):
            self.check_trader_inventory(self.talker.type)
            sentence = self.talker.get_random_opening_sentence(f"{self.talker.name}")
            return f"{sentence}\nBuy, Sell or Quit?"
        elif self.talker:
            return f"{self.talker.name} doesn't want to trade.", None
        else:
            return "There is no one to trade with.", None

    def check_trader_inventory(self, type):
        """Retrieve a list of items based on the specified `type` 
        calling get_entities_list method from Factory class and add 10
        random items to the trader's inventory if it is empty.

        Parameters
        ----------
        type : class
            The type of items to retrieve, which can be any Item subclass
            (Curse, Healer, ManaRecharger, Weapon or Armor)

        Returns
        -------
        None
            Add a sample of items matching the specified `type` to trader's
            inventory if it is empty and return None.
        """
        items_list = items().get_entities_list(type)
        if not self.talker.inventory:
            self.talker.inventory += random.sample(items_list, k=10)

    # -------------------------------------------------------------------------|
    # LOOK --------------------------------------------------------------------|
    # -------------------------------------------------------------------------|

    def look_command_handler(self):
        """Show a detailed description of the current room's scenario.

        Returns
        -------
        str
            A detailed description of the current room and its features
        """
        response = self.description
        for item in self.inventory:
            response += f"\nThere is a {item.name} here."
        for surrounding in self.environment:
            response += f"\nThere is a {surrounding.name} here."
        if self.talker:
            response += f"\nThere is {self.talker.name} here."
        if self.enemy and self.enemy.is_alive():
            response += f"\nThere is a {self.enemy.name} here, willing to kill you."
        elif self.enemy and not self.enemy.is_alive():
            response += f"\nThere the corpse of a {self.enemy.name} here."
        return response

    def look_at_command_handler(self, target, player):
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
        objects_to_check = [self, self.talker, self.enemy] + \
            self.inventory + self.environment + player.inventory
        for obj in objects_to_check:
            if obj and re.search(rf"\b\w*({''.join([f'{c}' for c in target])})\w*\b", obj.name.lower()) and len(set(target).intersection(set(obj.name.lower()))) >= 3:
                return obj.description
        return (f"I can't see any {target} here.")

    # -------------------------------------------------------------------------|
    # OPEN - ------------------------------------------------------------------|
    # -------------------------------------------------------------------------|

    def open_command_handler(self, *args):
        """_summary_

        Parameters
        ----------
        target : str
            _description_
        """
        target = args[1]
        for obj in self.environment:
            if target == obj.name.lower():
                if obj.openable:
                    return self.check_if_open(obj)
                else:
                    return f"You cannot open it."
            else:
                return "I beg your pardon?"
        else:
            return "There is nothing to open here."

    def check_if_open(self, obj):
        """_summary_

        Parameters
        ----------
        obj : Entity
        
        Returns
        -------
        response : str 
        """
        response = ""
        if obj.is_open == False and obj.name == "chest":
            response += "It's locked... Do you want to throw the Icosahedron and try to unlock it? Yes or No?"
            return response
        elif obj.is_open == False and obj.locked == False:
            response += f"You open the {obj.name}\n"
            response += "obj.description_when_opened"
            obj.is_open = True
        elif obj.is_open == False and obj.locked == True:
            response += f"You need to use a key to open this {obj.name}"
        else:
            response += f"This {obj.name} is already open."
        return response, None
