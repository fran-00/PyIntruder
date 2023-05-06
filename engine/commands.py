import re

import world.parser as parser

class Commands:
    def __init__(self, player, room):
        self.player = player
        self.room = room
        self.arguments_list = []

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

        if re.match(r'^(go\s)?(n(o(rth)?)?|s(o(uth)?)?|w(e(st)?)?|e(a(st)?)?)$', action):
            if not self.room.enemy or not self.room.enemy.is_alive():
                return (self.move(action))
            else:
                return ("You can't escape!")

        elif action in ["diagnose"]:
            return self.player.diagnose()

        elif re.match(r'^(i(nv(entory)?)?)$', action):
            self.arguments_list = [self.player.inventory, "my-inventory"]
            return (
                self.player.check_inventory,
                self.player.choose_item
            )

        elif re.match(r"^(a|attack)$", action):
            if self.room.enemy and self.room.enemy.is_alive():
                return self.player.attack()
            else:
                return "There is no one to attack here!"

        elif re.match(r'^(c(urse)?)$', action):
            self.arguments_list = [self.player.inventory, "Curse"]
            if self.room.enemy and self.room.enemy.is_alive():
                return (
                    self.player.check_inventory,
                    self.player.choose_item
                )
            else:
                return "There is no one to curse here!"
        
        elif re.match(r"^(run|flee|escape)$", action):
            if self.room.enemy and self.room.enemy.is_alive():
                return self.player.flee_from_fight()
            elif self.room.enemy and not self.room.enemy.is_alive():
                return "No need to escape, the enemy is dead!"
            else:
                return "There is nothing to run away from. If you want to escape just quit the game!"

        elif re.match(r'^(talk to)\s+(.+)$', action):
            talker_name = re.match(r'^(talk to)\s+(.+)$', action).group(2)
            return talker_name TODO:
        
        elif re.match(r'^(t(alk)?)$', action):
            if self.room.talker and not self.room.talker.trade:
                self.arguments_list = [None, "talk"]
                return (
                    self.room.check_if_trading,
                    self.room.dialogue
                )
            elif self.room.talker and self.room.talker.trade:
                self.arguments_list = [self.room.talker.inventory, "trade"]
                return (
                    self.room.check_if_trading,
                    self.player.trading_mode,
                    self.player.choose_item,
                )
            else:
                return "Hmmm... A tree looks at you expectantly, as if you seemed to be about to talk."

        elif re.match(r"^(p|pick up)$", action):
            self.arguments_list = [self.room.inventory, "pick-up"]
            return (
                self.player.check_inventory,
                self.player.choose_item
                )

        elif re.match(r'^(look)$', action):
            return self.player.look(self.room)
        
        elif re.match(r'^(get|pick up)\s+(.+)$', action):
            target = re.match(r'^(get|pick up)\s+(.+)$', action).group(2)
            return self.player.get_or_drop_item(self.room, self.player, target, "get")
        
        elif re.match(r'^(drop)\s+(.+)$', action):
            target = re.match(r'^(drop)\s+(.+)$', action).group(2)
            return self.player.get_or_drop_item(self.player, self.room, target, "drop")
    
        elif re.match(r"^(d|drop)$", action):
            self.arguments_list = [self.player.inventory, "drop"]
            return (
                self.player.check_inventory,
                self.player.choose_item
            )

        elif re.match(r'^(m(ap)?)$', action):
            return self.player.show_map()

        elif re.match(r'^(h(eal)?)$', action):
            self.arguments_list = [self.player.inventory, "Healer"]
            return (
                self.player.check_inventory,
                self.player.choose_item
            )

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
