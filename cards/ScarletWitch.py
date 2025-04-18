from cards import Card

class Scarletwitch(Card):
    def __init__(self, ally, status):
        super().__init__(2, 3, "Scarlet Witch", ally, status)
        self.description = "On Reveal: Replace this location with a new one."
    
    def onReveal(self, locationlist):
        self.location.changeLocation(self.location.randomLocation())

