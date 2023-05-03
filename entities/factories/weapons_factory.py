from ..entities_templates import Weapon


class WeaponsFactory:
    
    def __init__(self):
        
        self.manuport = Weapon(
            "Manuport",
            5,
            10,
        )
        self.sheet = Weapon(
            "polarized sheet",
            10,
            20,
        )
        self.polyhedron = Weapon(
            "Sharp Polyhedron",
            15,
            30,
        )
        self.armored_manuport = Weapon(
            "Armored Manuport",
            20,
            40,
        )
        self.polygon = Weapon(
            "Transparent Polygon",
            25,
            50,
        )
        
        self.wire = Weapon(
            "Wireless Wire",
            30,
            60,
        )
        self.branch = Weapon(
            "Armored Brench",
            35,
            70,
        )
        self.poly = Weapon(
            "N-dimensional Polytope",
            40,
            80,
        )
        self.device = Weapon(
            "Aperture Science Handheld Portal Device",
            45,
            90,
        )
        self.deliverance = Weapon(
            "Deliverance",
            50,
            100,
        )
        self.tesseract = Weapon(
            "Tesseract",
            55,
            110,
        )
        self.chuck = Weapon(
            "Chuck the plant",
            60,
            120,
        )
        self.attractor = Weapon(
            "Great Attractor",
            65,
            130,
        )
        self.cube = Weapon(
            "The Soul Cube",
            70,
            140,
        )
    
    def get_items_list(self):
        weapon_list = [
            self.manuport,
            self.sheet,
            self.polyhedron,
            self.armored_manuport,
            self.polygon,
            self.wire,
            self.branch,
            self.poly,
            self.device,
            self.deliverance,
            self.tesseract,
            self.chuck,
            self.attractor,
            self.cube
        ]
        return weapon_list