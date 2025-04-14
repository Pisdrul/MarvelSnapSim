from cards import Card

class Nova(Card):
    def __init__(self, ally, status):
        super().__init__(1, 1, "Nova", ally, status)
        self.description = "When this card is destroyed, +1 Power to all allies"
    
    def whenDestroyed(self, locationlist):
        
        for location in locationlist.values():
            if self.ally:
                for card in location.allies:
                    card.onreveal_buff += 1
            else:
                for card in location.enemies:
                    card.onreveal_buff += 1