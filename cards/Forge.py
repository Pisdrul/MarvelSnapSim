from cards import Card

class Forge(Card):
    def __init__(self, ally, status):
        super().__init__(2, 2, "Forge", ally, status)
        self.description = "On Reveal: Give the next card you play +2 Power"
    
    def onReveal(self, locationlist):
        self.status["onnextcardbeingplayed"].append(self)
    
    def nextCardBuff(self, card):
        if card.ally == self.ally and card != self:
            card.onreveal_buff += 2
            self.status["onnextcardbeingplayed"].remove(self)