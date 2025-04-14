from cards import Card

class Vulture(Card):
    def __init__(self, ally, status):
        super().__init__(3, 3, "Vulture", ally, status)
        self.description = "When this card moves, +6 Power."
    
    def onMove(self):
        self.onreveal_buff += 6