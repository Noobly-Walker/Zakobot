from bot.obj import Node
from bot.obj.Material import MAT

class Item:
    def __init__(self):
        self.recipes = []
        self.node = Node(parent="GameObject", name="Item")
        
    def add(self, toAdd):
        if self.quantity + toAdd > 0:
            self.quantity += toAdd
        else:
            pass #possibly return some failure code

    def subt(self, toSubtract):
        if self.quantity + toAdd > 0:
            self.quantity -= toSubtract
        else:
            pass #possibly return some failure code
