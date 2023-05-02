import random, json

from ..entities_templates import Armor


with open('entities/data/items_data.json') as f:
    items_data = json.load(f)


class ArmorsFactory:
    
    def __init__(self):
    
        self.rinas_armor = Armor(
            "Rina's Armor",
            items_data["armors"]["rina"],
            1,
            15,
            20,
        )
        self.fungine_armor = Armor(
            "Fungine Armor",
            items_data["armors"]["fungine"],
            1,
            15,
            20,
        )
        self.iron_armor = Armor(
            "Iron Armor",
            items_data["armors"]["iron"],
            1,
            15,
            20,
        )
        self.tesla_armor = Armor(
            "Tesla Armor",
            items_data["armors"]["tesla"],
            1,
            15,
            20,
        )
    
    def get_items_list(self):
        armors_list = [
            self.rinas_armor,
            self.fungine_armor,
            self.iron_armor,
            self.tesla_armor
        ]
        return armors_list