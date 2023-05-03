from ..entities_templates import Weapon


class WeaponsFactory:
    
    def __init__(self):
        
        self.manuport = Weapon(
            "Manuport",
            5
        )
        self.sheet = Weapon(
            "polarized sheet",
            10
        )
        self.polyhedron = Weapon(
            "Sharp Polyhedron",
            15
        )
        self.armored_manuport = Weapon(
            "Armored Manuport",
            20,
        )
        self.polygon = Weapon(
            "Transparent Polygon",
            25
        )
        self.wire = Weapon(
            "Wireless Wire",
            30
        )
        self.branch = Weapon(
            "Armored Brench",
            35
        )
        self.poly = Weapon(
            "N-dimensional Polytope",
            40
        )
        self.device = Weapon(
            "Aperture Science Handheld Portal Device",
            45
        )
        self.deliverance = Weapon(
            "Deliverance",
            50
        )
        self.tesseract = Weapon(
            "Tesseract",
            55
        )
        self.chuck = Weapon(
            "Chuck the plant",
            60
        )
        self.attractor = Weapon(
            "Great Attractor",
            65
        )
        self.cube = Weapon(
            "The Soul Cube",
            70
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