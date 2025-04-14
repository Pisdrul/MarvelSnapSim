from cards import Card

class Warpath(Card):
    def __init__(self, ally, status):
        super().__init__(4, 5, "Warpath", ally, status)
        self.description = "Ongoing: if any of your locations are empty, +5 Power."
        self.has_ongoing = True
    
    def applyOngoing(self, locationlist):
        if self.ally:
            if len(locationlist["location1"].allies) == 0 or len(locationlist["location2"].allies) == 0 or len(locationlist["location3"].allies) == 0:
                self.ongoing_to_apply.append(self)
        
        else:
            if len(locationlist["location1"].enemies) == 0 or len(locationlist["location2"].enemies) == 0 or len(locationlist["location3"].enemies) == 0:
                self.ongoing_to_apply.append(self)
    
    def ongoing(self, locationlist):
        self.ongoing_buff += 5