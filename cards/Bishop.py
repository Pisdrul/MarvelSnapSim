from cards import Card

class Bishop(Card):
    def __init__(self, ally, status):
        super().__init__(3, 2, "Bishop", ally, status)
        self.description = "After you play a card, this gains +1 Power"
    
    def onCardBeingPlayed(self, card):
        if card.ally == self.ally and card != self:
            self.onreveal_buff += 1