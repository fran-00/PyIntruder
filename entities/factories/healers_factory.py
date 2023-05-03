from ..entities_templates import Healer


class HealersFactory:
    
    def __init__(self):
        
        self.ats = Healer(
            "Advanced Tea Substitute",
            items_data["healers"]["ats"],
            2,
            1,
            3           
        )       
        self.gommo = Healer(
            "Gommo",
            items_data["healers"]["gommo"],
            2,
            1,
            3           
        )
        self.yellow_liquid = Healer(
            "Suspicious Yellow Liquid",
            items_data["healers"]["yellow liquid"],
            2,
            1,
            3           
        )
        self.golden_apple = Healer(
            "Golden Apple",
            items_data["healers"]["golden apple"],
            2,
            1,
            3           
        )
        self.nuka_cola = Healer(
            "Nuka Cola",
            items_data["healers"]["nuka cola"],
            2,
            1,
            3           
        )
        self.bandages = Healer(
            "bandages",
            items_data["healers"]["bandages"],
            2,
            1,
            3           
        )
        self.gummy_bears = Healer(
            "gummy bears",
            items_data["healers"]["gummy bears"],
            2,
            1,
            3           
        )
        self.mushrooms = Healer(
            "mushrooms",
            items_data["healers"]["mushrooms"],
            2,
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