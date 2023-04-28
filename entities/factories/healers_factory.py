import random, json

from ..entities_templates import Healer


with open('entities_data/items_data.json') as f:
    items_data = json.load(f)


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