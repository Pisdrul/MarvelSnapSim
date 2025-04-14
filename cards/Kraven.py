from cards import Card

class Kraven(Card):
    def __init__(self, ally, status):
        super().__init__(2, 3, "Kraven", ally, status)
        self.description = "When a card moves here, +2 Power"
    
    def onCardBeingMoved(self,card):
        if card.location == self.location:
            self.onreveal_buff += 2