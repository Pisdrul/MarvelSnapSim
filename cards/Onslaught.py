from cards import Card

class Onslaught(Card):
    def __init__(self, ally, status):
        super().__init__(6, 7, "Onslaught", ally, status)
        self.description = "Ongoing: Your Ongoings here are doubled."
        self.has_ongoing = True
        self.onslaught = True
    
    def applyOngoing(self, locationlist):
        if self.ally:
            for unit in self.location.allies:
                if unit != self and not unit.onslaught:
                    unit.applyOngoing(locationlist)
        else:
            for unit in self.location.enemies:
                if unit != self and not unit.onslaught:
                    unit.applyOngoing(locationlist)