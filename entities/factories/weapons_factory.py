import random, json

from ..entities_templates import Weapon


with open('entities/data/items_data.json') as f:
    items_data = json.load(f)


class WeaponsFactory:
    
    def __init__(self):
        
        self.manuport = Weapon(
            "manuport",
            items_data["weapons"]["manuport"],
            1,
            15,
            20,
        )
        self.sheet = Weapon(
            "polarized sheet",
            items_data["weapons"]["polarized sheet"],
            1,
            15,
            20,
        )
        self.polyhedron = Weapon(
            "sharp polyhedron",
            items_data["weapons"]["sharp polyhedron"],
            1,
            15,
            20,
        )
        self.armored_manuport = Weapon(
            "armored manuport",
            items_data["weapons"]["armored manuport"],
            1,
            15,
            20,
        )
        self.polygon = Weapon(
            "transparent polygon",
            items_data["weapons"]["transparent polygon"],
            1,
            15,
            20,
        )
        
        self.wire = Weapon(
            "wireless wire",
            items_data["weapons"]["wireless wire"],
            1,
            15,
            20,
        )
        self.branch = Weapon(
            "armored brench",
            items_data["weapons"]["armored brench"],
            1,
            15,
            20,
        )
        self.poly = Weapon(
            "n-dimensional polytope",
            items_data["weapons"]["polytope"],
            1,
            15,
            20,
        )
        self.device = Weapon(
            "Aperture Science Handheld Portal Device",
            items_data["weapons"]["ashpd"],
            1,
            15,
            20,
        )
        self.deliverance = Weapon(
            "Deliverance by Tediore (Shotgun)",
            items_data["weapons"]["deliverance"],
            1,
            15,
            20,
        )
        self.tesseract = Weapon(
            "name",
            items_data["weapons"]["tesseract"],
            1,
            15,
            20,
        )
        self.chuck = Weapon(
            "Chuck the plant",
            items_data["weapons"]["chuck"],
            1,
            15,
            20,
        )
        self.attractor = Weapon(
            "great attractor",
            items_data["weapons"]["great attractor"],
            1,
            15,
            20,
        )
        self.cube = Weapon(
            "The Soul Cube",
            items_data["weapons"]["soul Cube"],
            1,
            15,
            20,
        )