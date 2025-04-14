from cards import Card

class Antman(Card):
    def __init__(self, ally, status):
        super().__init__(1, 1, "Antman", ally, status)
        self.description = "Ongoing: If your side of this location is full, +4 power."
        self.has_ongoing = True
    
    def applyOngoing(self, locationlist):
        if self.ally:
            if len(self.location.allies) == 4:
                self.ongoing_to_apply.append(self)
        else:
            if len(self.location.enemies) == 4:
                self.ongoing_to_apply.append(self)
    
    def ongoing(self, locationlist):
        self.ongoing_buff += 4