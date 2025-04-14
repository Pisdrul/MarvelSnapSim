from cards import Card

class Punisher(Card):
    def __init__(self, ally, status):
        super().__init__(3, 3, "Punisher", ally, status)
        self.description = "Ongoing: +1 power for each enemy card here."
        self.has_ongoing = True

    def applyOngoing(self, locationlist):
        self.ongoing_to_apply.append(self)
    
    def ongoing(self, locationlist):
        if self.ally:
            self.ongoing_buff += len(self.location.enemies)
        else:
            self.ongoing_buff += len(self.location.allies)