from cards import Card

class Morbius(Card):
    def __init__(self, ally, status):
        super().__init__(2, 0, "Morbius", ally, status)
        self.description = "Ongoing: +2 Power for each card you discarded this game"
        self.has_ongoing = True
    
    def applyOngoing(self, locationlist):
        self.ongoing_to_apply.append(self)
    
    def ongoing(self, locationlist):
        if self.ally:
            self.ongoing_buff += 2*len(self.status["alliesdiscarded"])
        else:
            self.ongoing_buff += 2*len(self.status["enemiesdiscarded"])