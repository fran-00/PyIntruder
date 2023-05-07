from ..entities_templates import Healer


class HealersFactory:
    
    def __init__(self):
        
        self.ats = Healer(
            "Advanced Tea Substitute",
            1,       
        )       
        self.gommo = Healer(
            "Gommo",
            1,       
        )
        self.yellow_liquid = Healer(
            "Suspicious Yellow Liquid",
            1,       
        )
        self.golden_apple = Healer(
            "Golden Apple",
            1,       
        )
        self.nuka_cola = Healer(
            "Nuka Cola",
            1,       
        )
        self.bandages = Healer(
            "Bandages",
            1,       
        )
        self.gummy_bears = Healer(
            "Gummy Bears",
            1,       
        )
        self.mushrooms = Healer(
            "Mushrooms",
            1,       
        )
    
    def get_items_list(self):
        healers_list = [
            self.ats,
            self.gommo,
            self.yellow_liquid,
            self.golden_apple,
            self.nuka_cola,
            self.bandages,
            self.gummy_bears,
            self.mushrooms
        ]
        return healers_list