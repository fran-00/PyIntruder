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
            'INVENTORY': r'^(i(nv(entory)?)?)$',
            'ATTACK': r'^(a(ttack)?)$',
            'CURSE': r'^(c(urse)?)$',
            'RUN': r'^(run|flee|escape)$',
            'TALK TO': r'^(talk to)\s+(.+)$',
            'TRADE': r'^(trade)$',
            'GET ITEM': r'^(get|pick up)\s+(.+)$',
            'GET FROM LIST': r'^(get|pick up)$',
            'DROP ITEM': r'^(drop)\s+(.+)$',
            'DROP FROM LIST': r'^(d(rop)?)$',
            'HEAL': r'^(h(eal)?)$',
            'MAP': r'^(m(ap)?)$'
        }

    def get_room_description(self):
        self.room = parser.tile_at(self.player.x, self.player.y)
        if self.room.enemy is None:
            return (f"***{self.room.name}***\n> {self.room.description}")
        elif self.room.enemy.is_alive():
            return (f"{self.room.enemy.description_if_alive}")
        elif not self.room.enemy.is_alive():
            return (f"{self.room.enemy.description_if_dead}")

    def choose_action(self, action=str):
        """Chooses an action based on the given input string and returns its result.

        Args:
            action (str): The input string representing the action to be taken.

        Returns:
            # TODO

        """
        self.player.turn += 1

        for command, regex in self.commands_dict.items():
            if re.match(regex, action):
                if command == "DIRECTIONS":
                    if not self.room.enemy or not self.room.enemy.is_alive():
                        return (self.move(action))
                    else:
                        return ("You can't escape!")

                elif command == "DIAGNOSE":
                    return self.player.diagnose()

                elif command == "LOOK":
                    return self.player.look(self.room)

                elif command == "INVENTORY":
                    self.arguments_list = [self.player.inventory, "my-inventory"]
                    return (
                        self.player.check_inventory,
                        self.player.choose_item
                    )

                elif command == "ATTACK":
                    if self.room.enemy and self.room.enemy.is_alive():
                        return self.player.attack()
                    else:
                        return "There is no one to attack here!"

                elif command == "CURSE":
                    self.arguments_list = [self.player.inventory, "Curse"]
                    if self.room.enemy and self.room.enemy.is_alive():
                        return (
                            self.player.check_inventory,
                            self.player.choose_item
                        )
                    else:
                        return "There is no one to curse here!"

                elif command == "RUN":
                    if self.room.enemy and self.room.enemy.is_alive():
                        return self.player.flee_from_fight()
                    elif self.room.enemy and not self.room.enemy.is_alive():
                        return "No need to escape, the enemy is dead!"
                    else:
                        return "There is nothing to run away from. If you want to escape just quit the game!"

                elif command == "TALK TO":
                    target = re.match(regex, action).group(2)
                    if self.room.talker and not self.room.talker.trade:
                        return ""
                    else:
                        self.arguments_list = [None, "talk"]
                        return (
                            self.room.check_if_trading,
                            self.room.dialogue
                        )

                elif command == "TRADE":
                    if self.room.talker and self.room.talker.trade:
                        self.arguments_list = [self.room.talker.inventory, "trade"]
                    else:
                        self.arguments_list = [None]
                    return (
                        self.room.trade,
                        self.player.trading_mode,
                        self.player.choose_item,
                    )

                elif command == "GET FROM LIST":
                    self.arguments_list = [self.room.inventory, "pick-up"]
                    return (
                        self.player.check_inventory,
                        self.player.choose_item
                    )

                elif command == "DROP FROM LIST":
                    self.arguments_list = [self.player.inventory, "drop"]
                    return (
                        self.player.check_inventory,
                        self.player.choose_item
                    )

                elif command == "GET ITEM":
                    target = re.match(regex, action).group(2)
                    return self.player.get_or_drop_item(self.room, self.player, target, "get")

                elif command == "DROP ITEM":
                    target = re.match(regex, action).group(2)
                    return self.player.get_or_drop_item(self.player, self.room, target, "drop")

                elif command == "HEAL":
                    if self.player.hp == self.player.max_hp:
                        return f"You are already in good health."
                    else:
                        self.arguments_list = [self.player.inventory, "Healer"]
                        return (
                            self.player.check_inventory,
                            self.player.choose_item
                        )

                elif command == "MAP":
                    return self.player.show_map()

                else:
                    return ("I beg your pardon?")

    def move(self, action):
        """Move the player in the specified direction if possible and return the room description.

        Args:
            room (Room(MapTile)): The current room from world.tiles
            player (Player): The player object.

        Returns:
            str: Room's description if player is able to move, or an error message if the requested direction is not valid.

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
