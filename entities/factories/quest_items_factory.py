from ..entities_templates import Item


class QuestItemsFactory:
    
    def __init__(self):
        
        self.specimen = Item(
            "The Specimen",
            10
        )
        self.bottle = Item(
            "bottle",
            10
        )