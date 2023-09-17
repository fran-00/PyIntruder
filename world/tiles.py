import random

from entities.factory import EntitiesFactory as entities
from world.map_tile import MapTile


class StartTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Clearing'
        super().__init__(x, y)
        self.environment = [entities().car, entities().table]


class LittleoTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Little(o) Shop'
        super().__init__(x, y)
        self.talker = entities().littleo


class BlacksmithTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Blacksmith'
        super().__init__(x, y)
        self.talker = entities().blacksmith


class ChestTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Chest'
        super().__init__(x, y)
        self.environment = [entities().chest]

    def handle_event(self, *args):
        player = args[0]
        action = args[-1]

        match action.lower():
            case "n" | "no":
                return "Ok, this chest will remain closed."
            case "y" | "yes":
                return self.random_chest_event(player)
            case _:
                return "Invalid choice."
    
    def random_chest_event(self, player):
        ico = random.randint(1, 20)
        response = "You roll the dice..."
        gold = 0
        match ico:
            case 20:
                gold += 1000
                response += (
                    f"Dice says 20! IT'S INCREDIBLE!!!"
                    f"You found {gold} § inside of it!"
                    )
            case x if 15 < x < 20:
                gold += random.randint(300, 499)
                response += ( 
                    f"Dice says {ico}! Not bad!"
                    f"You found {gold} § inside of it!"
                    )
            case x if 11 < x < 16:
                gold += random.randint(150, 299)
                response += (
                    f"Dice says {ico}! Good!"
                    f"You found {gold} § inside of it!"
                    )
            case x if 7 < x < 12:
                gold += random.randint(50, 149)
                response += (
                    f"> Dice says {ico}! Hmmm..."
                    f"Only {gold} §..."
                    )
            case x if 3 < x < 8:
                gold += random.randint(0, 50)
                response += (
                    f"{ico}!"
                    )
            case x if 4 < x < 0:
                response += (
                    f"{ico}!"
                    )
            case 0:
                response += (
                    f"{ico}!"
                )
        player.gold += gold
        response += f"You now have {player.gold} §."
        return response


class FernsTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Ferns'
        super().__init__(x, y)
        self.talker = entities().ferns


class FountainTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Fountain'
        super().__init__(x, y)
        self.water = True


class IntruderTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Intruder'
        super().__init__(x, y)
        self.talker = entities().intruder


class RiverTile(MapTile):
    def __init__(self, x, y):
        self.name = 'River'
        super().__init__(x, y)


class OakTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Oak'
        super().__init__(x, y)
        self.talker = entities().oak


class PathTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Path'
        super().__init__(x, y)


class TempleTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Temple'
        super().__init__(x, y)
        self.talker = entities().monk


class VictoryTile(MapTile):
    def __init__(self, x, y):
        self.name = 'Victory'
        super().__init__(x, y)
