from cards import Card

class Namor(Card):
    def __init__(self, ally, status):
        super().__init__(4, 6, "Namor", ally, status)
        self.description = "+5 Power if this is your only card here."
        self.has_ongoing = True
    
    def applyOngoing(self, locationlist):
        if self.ally:
            if len(self.location.allies) == 1:
                self.ongoing_to_apply.append(self)
        else:
            if len(self.location.enemies) == 1:
                self.ongoing_to_apply.append(self)
    
    def ongoing(self, locationlist):
        self.ongoing_buff += 5
