from ..entities_templates import Surrounding


class SurroundingsFactory:
    
    def __init__(self):
        
        self.specimen = Surrounding(
            "your car",
            [],
            openable = True,
        )
        self.specimen = Surrounding(
            "chest",
            [],
            openable = True,
        )