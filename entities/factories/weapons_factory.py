import random, json

from ..entities_templates import Weapon


with open('entities/data/items_data.json') as f:
    items_data = json.load(f)


class WeaponsFactory:
    
    def __init__(self):
        
        self.manuport = Weapon(
            "manuport",
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
            "sharp polyhedron",
            1,
            15,
            20,
        )
        self.armored_manuport = Weapon(
            "armored manuport",
            1,
            15,
            20,
        )
        self.polygon = Weapon(
            "transparent polygon",
            1,
            15,
            20,
        )
        
        self.wire = Weapon(
            "wireless wire",
            1,
            15,
            20,
        )
        self.branch = Weapon(
            "armored brench",
            1,
            15,
            20,
        )
        self.poly = Weapon(
            "n-dimensional polytope",
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
            "Deliverance by Tediore (Shotgun)",
            1,
            15,
            20,
        )
        self.tesseract = Weapon(
            "name",
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
            "great attractor",
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