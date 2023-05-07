from ..entities_templates import MissionRelatedItem


class MissionRelatedItemsFactory:
    
    def __init__(self):
        
        self.specimen = MissionRelatedItem(
            "The Specimen",
        )
        self.bottle = MissionRelatedItem(
            "bottle",
            openable = True
        )