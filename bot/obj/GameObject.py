class GameObject:
    def __init__(self):
        self.quantity = 0
        
    def add(self, toAdd):
        self.quantity += toAdd

    def subt(self, toSubtract):
        self.quantity -= toSubtract

    def clear(self):
        self.quantity = 0

    def ct(self):
        return self.quantity
