import items

class EnvironmentalObjects():
    def __init__(self):
        raise NotImplementedError("Do not create raw NPC objects.")
    
    def __str__(self):
        return self.name


class Car(EnvironmentalObjects):
    def __init__(self):
        self.name = "car"
        self.description = "It's a little white Panda. Inside your car there's a big bottle of water, too heavy to carry in your backpack. You can fill your bottle from it, though."
        self.inventory =  [items.Bottle()]
        self.can_be_open = True
        
class Chest(EnvironmentalObjects):
    def __init__(self):
        self.name = "chest"
        self.description = "The chest is made of mahogany and has a solid appearance."
        self.inventory =  []
        self.can_be_open = False