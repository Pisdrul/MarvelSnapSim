from cards import Card

class Cloak(Card):
    def __init__(self, ally, status):
        super().__init__(2, 4, "Cloak", ally, status)
        self.description = "On Reveal: Next turn, both players can move cards to this location."
        self.turnToCheck = 0
    
    def onReveal(self, locationlist):
        self.turnToCheck = self.status["turncounter"] + 1
        self.locationToMove = self.location
    
    def startOfTurn(self):
        if self.turnToCheck == self.status["turncounter"]:
            self.location.location_can_be_moved_to = True