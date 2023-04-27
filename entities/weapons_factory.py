import random, json

from .entities_templates import Weapon


with open('entities_data/items_data.json') as f:
    items_data = json.load(f)

class WeaponsFactory:
    
    def __init__(self):
        self.wireless_wire = Weapon(
            "Manuport",
            items_data["weapons"]["manuport"],
            1,
            15,
            20,
        )
        self.name = Weapon(
            "polarized sheet",
            items_data["weapons"]["polarized_sheet"],
            1,
            15,
            20,
        )
        self.name = Weapon(
            "sharp polyhedron",
            items_data["weapons"]["sharp polyhedron"],
            1,
            15,
            20,
        )
        self.name = Weapon(
            "armored manuport",
            items_data["weapons"]["armored manuport"],
            1,
            15,
            20,
        )
        self.name = Weapon(
            "transparent polygon",
            items_data["weapons"]["transparent polygon"],
            1,
            15,
            20,
        )
        
        self.name = Weapon(
            "wireless wire",
            items_data["weapons"]["name"],
            1,
            15,
            20,
        )
        self.name = Weapon(
            "armored brench",
            items_data["weapons"]["armored brench"],
            1,
            15,
            20,
        )
        self.name = Weapon(
            "n-dimensional polytope",
            items_data["weapons"]["polytope"],
            1,
            15,
            20,
        )
        self.name = Weapon(
            "Aperture Science Handheld Portal Device",
            items_data["weapons"]["ashpd"],
            1,
            15,
            20,
        )
        self.name = Weapon(
            "Deliverance by Tediore (Shotgun)",
            items_data["weapons"]["deliverance"],
            1,
            15,
            20,
        )
        self.name = Weapon(
            "name",
            items_data["weapons"]["tesseract"],
            1,
            15,
            20,
        )
        self.name = Weapon(
            "Chuck the plant",
            items_data["weapons"]["chuck"],
            1,
            15,
            20,
        )
        self.name = Weapon(
            "great attractor",
            items_data["weapons"]["great attractor"],
            1,
            15,
            20,
        )
        self.name = Weapon(
            "The Soul Cube",
            items_data["weapons"]["soul Cube"],
            1,
            15,
            20,
        )