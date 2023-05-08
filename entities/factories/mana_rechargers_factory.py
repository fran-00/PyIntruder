from ..entities_templates import ManaRecharger

class ManaRechargersFactory:
    
    def __init__(self):
        self.name = ManaRecharger(
            "name",
            10
        )