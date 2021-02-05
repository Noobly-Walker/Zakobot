from bot.obj import GameObject

class Item(GameObject):
    def __init__(self):
        self.recipes = []
        
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
