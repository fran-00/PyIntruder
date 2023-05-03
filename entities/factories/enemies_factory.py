from ..entities_templates import Enemy


class EnemiesFactory:
    def __init__(self):
        # Level 1
        self.gel_cube = Enemy(
            "Gelatinous Cube",
            1,
            20,
            10
        )
        self.squirrel = Enemy(
            "Ravenous Squirrel",
            1,
            30,
            15
        )
        self.helicopter = Enemy(
            "Helicopter",
            1,
            40,
            20
        )

        # Level 2
        self.hunter = Enemy(
            "Mushroom Hunter",
            2,
            50,
            25
        )
        self.bug = Enemy(
            "Bug in the Program",
            2,
            60,
            30
        )
        self.eyes = Enemy(
            "Floating Eyes",
            3,
            70,
            35
        )


        # Level 3
        self.ants = Enemy(
            "ants infected by a fungus",
            3,
            80,
            40
        )
        self.trog = Enemy(
            "Trog",
            3,
            90,
            45
        )
        self.uncanny = Enemy(
            "Uncanny Valley",
            4,
            100,
            50
        )

        # level 4
        self.gnome = Enemy(
            "Gnome armed with an ax",
            4,
            120,
            60
        )

        # Level 5
        self.ostoyae = Enemy(
            "Armillaria Ostoyae",
            5,
            150,
            75
        )

