from cards import Card

class Sabretooth(Card):
    def __init__(self, ally, status):
        super().__init__(3, 5, "Sabretooth", ally, status)
        self.description = "When this is destroyed, return it to your hand. It costs 0."
    
    def whenDestroyed(self, locationlist):
        self.cost = 0
        if self.ally:
            self.status["allyhand"].append(self)
        else:
            self.status["enemyhand"].append(self)