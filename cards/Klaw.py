from cards import Card

class Klaw(Card):
    def __init__(self, ally, status):
        super().__init__(1, 4, "Klaw", ally, status)
        self.description = "Ongoing: The location to the right has +7 Power."
        self.has_ongoing = True

    def ongoing(self, location):
        if self.ally:
            location.allies_power_buff_sum += 7
        else:
            location.enemies_power_buff_sum += 7
    
    def applyOngoing(self, locationlist):
        location = self.location.returnRightOrLeftLocation(1)
        if location != None:
            location.ongoing_to_apply.append(self)