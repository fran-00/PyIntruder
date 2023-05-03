from ..entities_templates import Item


class QuestItemsFatory:
    
    def __init__(self):
        
        self.specimen = Item(
            "The Specimen",
            1,
            10
        )
        self.bottle = Item(
            "bottle",
            1,
            10
        )