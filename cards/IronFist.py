from cards import Card

class IronFist(Card):
    def __init__(self, ally, status):
        super().__init__(1, 2, "Iron Fist", ally, status)
        self.description = "On Reveal: After you play your next card, move it one location to the left."
    
    def onReveal(self, locationlist):
        self.status["onnextcardbeingplayed"].append(self)
    
    def nextCardBuff(self, card):
        if card.ally == self.ally and card != self:
            print("Here for iron fist")
            self.status["onnextcardbeingplayed"].remove(self)
            newloc= card.location.returnRightOrLeftLocation(-1)
            if newloc != None:
                card.move(newloc)