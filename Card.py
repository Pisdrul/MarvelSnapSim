class Card:
    def __init__(self, cost, power, name):
        self.cost = cost
        self.power = power
        self.name = name
        
    def __repr__(self):
        return f"{self.power}"
    
    def onReveal(self):
        print("Revealed ",self.name)