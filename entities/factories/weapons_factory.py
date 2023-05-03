from ..entities_templates import Weapon


class WeaponsFactory:
    
    def __init__(self):
        
        self.manuport = Weapon(
            "Manuport",
            1,
            15,
            20,
        )
        self.sheet = Weapon(
            "polarized sheet",
            1,
            15,
            20,
        )
        self.polyhedron = Weapon(
            "Sharp Polyhedron",
            1,
            15,
            20,
        )
        self.armored_manuport = Weapon(
            "Armored Manuport",
            1,
            15,
            20,
        )
        self.polygon = Weapon(
            "Transparent Polygon",
            1,
            15,
            20,
        )
        
        self.wire = Weapon(
            "Wireless Wire",
            1,
            15,
            20,
        )
        self.branch = Weapon(
            "Armored Brench",
            1,
            15,
            20,
        )
        self.poly = Weapon(
            "N-dimensional Polytope",
            1,
            15,
            20,
        )
        self.device = Weapon(
            "Aperture Science Handheld Portal Device",
            1,
            15,
            20,
        )
        self.deliverance = Weapon(
            "Deliverance",
            1,
            15,
            20,
        )
        self.tesseract = Weapon(
            "Tesseract",
            1,
            15,
            20,
        )
        self.chuck = Weapon(
            "Chuck the plant",
            1,
            15,
            20,
        )
        self.attractor = Weapon(
            "Great Attractor",
            1,
            15,
            20,
        )
        self.cube = Weapon(
            "The Soul Cube",
            1,
            15,
            20,
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