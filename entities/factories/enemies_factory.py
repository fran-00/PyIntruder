from ..entities_templates import Enemy
import random, json


with open('entities/data/enemies_data.json') as ef:
    enemies_data = json.load(ef)


class EnemiesFactory:
    def __init__(self):
        # Level 1
        self.gel_cube = Enemy(
            "Gelatinous Cube",
            enemies_data["gel cube"]["intro_alive"],
            1,
            20,
            10
        )
        self.squirrel = Enemy(
            "Ravenous Squirrel",
            enemies_data["squirrel"]["intro_alive"],
            1,
            30,
            15
        )
        self.helicopter = Enemy(
            "Helicopter",
            enemies_data["helicopter"]["intro_alive"],
            1,
            40,
            20
        )

        # Level 2
        self.hunter = Enemy(
            "Mushroom Hunter",
            enemies_data["hunter"]["intro_alive"],
            2,
            50,
            25
        )
        self.bug = Enemy(
            "Bug in the Program",
            enemies_data["bug"]["intro_alive"],
            2,
            60,
            30
        )
        self.eyes = Enemy(
            "Floating Eyes",
            enemies_data["eyes"]["intro_alive"],
            3,
            70,
            35
        )


        # Level 3
        self.ants = Enemy(
            "ants infected by a fungus",
            enemies_data["ants"]["intro_alive"],
            3,
            80,
            40
        )
        self.trog = Enemy(
            "Trog",
            enemies_data["trog"]["intro_alive"],
            3,
            90,
            45
        )
        self.uncanny = Enemy(
            "Uncanny Valley",
            enemies_data["uncanny"]["intro_alive"],
            4,
            100,
            50
        )

        # level 4
        self.gnome = Enemy(
            "Gnome armed with an ax",
            enemies_data["gnome"]["intro_alive"],
            4,
            120,
            60
        )

        # Level 5
        self.ostoyae = Enemy(
            "Armillaria Ostoyae",
            enemies_data["ostoyae"]["intro_alive"],
            5,
            150,
            75
        )

