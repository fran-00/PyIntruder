import re

import world.parser as parser


class Commands:
    def __init__(self, player, room):
        self.player = player
        self.room = room
        self.arguments_list = []
        self.commands_dict = {
            'DIRECTIONS': r'^(go\s)?(n(o(rth)?)?|s(o(uth)?)?|w(e(st)?)?|e(a(st)?)?)$',
            'NORTH': r'^(go\s)?n(o(rth)?)?$',
            'SOUTH': r'^(go\s)?s(o(uth)?)?$',
            'WEST': r'^(go\s)?w(e(st)?)?$',
            'EAST': r'^(go\s)?e(a(st)?)?$',
            'DIAGNOSE': r'^(diagnose)$',
            'LOOK': r'^(l(ook)?)$',
            'LOOK AT': r'^(look at|examine|watch)\s+(.+)$',
            'INVENTORY': r'^(i(nv(entory)?)?)$',
            'ATTACK': r'^(a(ttack)?)$',
            'CURSE': r'^(c(urse)?)$',
            'RUN': r'^(run|flee|escape)$',
            'TALK TO': r'^(talk to)\s+(.+)$',
            'TALK': r'^(talk)$',
            'TRADE': r'^(trade)$',
            'GET ITEM': r'^(get|pick up)\s+(.+)$',
            'GET FROM LIST': r'^(get|pick up)$',
            'DROP ITEM': r'^(drop)\s+(.+)$',
            'DROP FROM LIST': r'^(d(rop)?)$',
            'HEAL': r'^(h(eal)?)$',
            'OPEN OBJECT': r'^(open)\s+(.+)$',
            'OPEN': r'^(open)$',
            'MAP': r'^(m(ap)?)$'
        }

    def get_room_description(self):
        """Show a description for the room Player is currently in.

        Check if there is an enemy in the room and if it is alive or not.
        If there is no enemy, it return the name and description of the current room. 
        If there is an enemy, it return a description if is alive and another
        if is dead.

        Returns
        -------
        string
            A description of the current room or enemy
        """
        self.room = parser.tile_at(self.player.x, self.player.y)
        if self.room.enemy is None:
            return (f"<h2>{self.room.name}</h2><p>{self.room.description}</p>")
        elif self.room.enemy.is_alive():
            return (f"{self.room.enemy.description_if_alive}")
        elif not self.room.enemy.is_alive():
            return (f"{self.room.enemy.description_if_dead}")

    def choose_action(self, action=str):
        """Choose an action based on the given input string and returns its result.

        Parameters
        ----------
        action : str
            The input string representing the action to be taken.

        Returns
        -------
        str
            The string to show depends on the command entered, for each of
            them a method of Player class or of MapTile class is called.
        """
        self.player.turn += 1

        for command, regex in self.commands_dict.items():
            if re.match(regex, action):
                if command == "ATTACK":
                    return (
                        self.player.attack_command_handler()
                        if self.room.enemy and self.room.enemy.is_alive()
                        else "There is no one to attack here!"
                    )
                elif command == "CURSE":
                    self.arguments_list = [self.player.inventory, "Curse"]
                    return (
                        (self.player.check_inventory, self.player.choose_item)
                        if self.room.enemy and self.room.enemy.is_alive()
                        else "There is no one to curse here!"
                    )
                elif command == "DIAGNOSE":
                    return self.player.diagnose_command_handler()

                elif command == "DIRECTIONS":
                    return (
                        (self.move(action))
                        if not self.room.enemy or not self.room.enemy.is_alive()
                        else "You can't escape!"
                    )
                elif command == "DROP FROM LIST":
                    self.arguments_list = [self.player.inventory, "drop"]
                    return (
                        self.player.check_inventory,
                        self.player.choose_item
                    )
                elif command == "DROP ITEM":
                    target = re.match(regex, action)[2]
                    return self.player.get_and_drop_command_handler(self.player, self.room, target, "drop")
                elif command == "GET FROM LIST":
                    self.arguments_list = [self.room.inventory, "pick-up"]
                    return (
                        self.player.check_inventory,
                        self.player.choose_item
                    )
                elif command == "GET ITEM":
                    target = re.match(regex, action)[2]
                    return self.player.get_and_drop_command_handler(self.room, self.player, target, "get")
                elif command == "HEAL":
                    if self.player.hp == self.player.max_hp:
                        return "You are already in good health."
                    self.arguments_list = [self.player.inventory, "Healer"]
                    return (
                        self.player.check_inventory,
                        self.player.choose_item
                    )
                elif command == "INVENTORY":
                    return self.player.check_inventory(self.player.inventory, "my-inventory")

                elif command == "LOOK AT":
                    target = re.match(regex, action)[2]
                    return self.room.look_at_command_handler(target, self.player)

                elif command == "LOOK":
                    return self.room.look_command_handler()

                elif command == "MAP":
                    return self.player.show_map()
                elif command == "OPEN OBJECT":
                    target = re.match(regex, action)[2]
                    self.arguments_list = [self.player, target]
                    return (
                        self.room.open_command_handler,
                        self.room.handle_event
                    )
                elif command == "OPEN":
                    return "What do you want to open?"
                elif command == "RUN":
                    if self.room.enemy and self.room.enemy.is_alive():
                        return self.player.flee_from_fight()
                    elif self.room.enemy and not self.room.enemy.is_alive():
                        return "No need to escape, the enemy is dead!"
                    else:
                        return "There is nothing to run away from. If you want to escape just quit the game!"

                elif command == "TALK TO":
                    target = re.match(regex, action)[2]
                    self.arguments_list = [self.player, target]
                    return (
                        self.room.choose_talking_npc,
                        self.room.dialogue,
                        self.room.dialogue,
                        self.room.dialogue,
                        self.room.dialogue,
                        self.room.dialogue
                    )
                elif command == "TALK":
                    return "Hmmm ... A tree looks at you expectantly, as if you seemed to be about to talk."

                elif command == "TRADE":
                    self.arguments_list = [self.room.talker.inventory, "trade"]
                    return (
                        self.room.trade,
                        self.player.trading_mode,
                        self.player.choose_item,
                    )
        return ("I beg your pardon?")

    def move(self, action):
        """Move the player in the specified direction if possible and return the room description.

        Parameters
        ----------
        action : str
            The direction Player wants to go.

        Returns
        -------
        str
            Room's description if player is able to move, or an error
            message if the requested direction is not valid.

        """
        if re.match(r'^(go\s)?n(o(rth)?)?$', action) and parser.tile_at(self.room.x, self.room.y - 1):
            self.player.move_north()
        elif re.match(r'^(go\s)?s(o(uth)?)?$', action) and parser.tile_at(self.room.x, self.room.y + 1):
            self.player.move_south()
        elif re.match(r'^(go\s)?e(a(st)?)?$', action) and parser.tile_at(self.room.x + 1, self.room.y):
            self.player.move_east()
        elif re.match(r'^(go\s)?w(e(st)?)?$', action) and parser.tile_at(self.room.x - 1, self.room.y):
            self.player.move_west()
        else:
            return "You can't go that way!"
        return self.get_room_description()
