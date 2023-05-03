from ..entities_templates import Item


class QuestItemsFatory:
    
    def __init__(self):
        
        self.specimen = Item(
            "The Specimen",
            items_data["mission items"]["specimen"],
            1,
            10
        )
        self.bottle = Item(
            "bottle",
            items_data["mission items"]["bottle"],
            1,
            10
        )