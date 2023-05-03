from ..entities_templates import Armor


class ArmorsFactory:
    
    def __init__(self):
    
        self.rinas_armor = Armor(
            "Rina's Armor",
            15,
            20,
        )
        self.fungine_armor = Armor(
            "Fungine Armor",
            15,
            20,
        )
        self.iron_armor = Armor(
            "Iron Armor",
            15,
            20,
        )
        self.tesla_armor = Armor(
            "Tesla Armor",
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