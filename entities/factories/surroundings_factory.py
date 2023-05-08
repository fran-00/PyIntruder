from ..entities_templates import Surrounding


class SurroundingsFactory:
    
    def __init__(self):
        
        self.specimen = Surrounding(
            "car",
            [],
            openable = True,
        )
        self.chest = Surrounding(
            "chest",
            [],
            openable = True,
        )