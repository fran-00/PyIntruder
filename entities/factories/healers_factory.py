from ..entities_templates import Healer


class HealersFactory:
    
    def __init__(self):
        
        self.ats = Healer(
            "Advanced Tea Substitute",
            1,
            3           
        )       
        self.gommo = Healer(
            "Gommo",
            1,
            3           
        )
        self.yellow_liquid = Healer(
            "Suspicious Yellow Liquid",
            1,
            3           
        )
        self.golden_apple = Healer(
            "Golden Apple",
            1,
            3           
        )
        self.nuka_cola = Healer(
            "Nuka Cola",
            1,
            3           
        )
        self.bandages = Healer(
            "Bandages",
            1,
            3           
        )
        self.gummy_bears = Healer(
            "Gummy Bears",
            1,
            3           
        )
        self.mushrooms = Healer(
            "Mushrooms",
            1,
            3           
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