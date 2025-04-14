from cards import Card

class Lizard(Card):
    def __init__(self, ally, status):
        super().__init__(2, 5, "Lizard", ally, status)
        self.description = "Ongoing: -4 power if your opponent has 4 cards here."
        self.has_ongoing = True

    def applyOngoing(self, locationlist):
        if self.ally:
            if len(self.location.enemies) == 4:
                self.ongoing_to_apply.append(self)
        else:
            if len(self.location.allies) == 4:
                self.ongoing_to_apply.append(self)
    
    def ongoing(self, locationlist):
        self.ongoing_buff -= 4