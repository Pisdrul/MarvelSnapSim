from cards import Card

class Mrfantastic(Card):
    def __init__(self, ally, status):
        super().__init__(3, 2, "Mr Fantastic", ally, status)
        self.description = "Ongoing: The location to the left and right have +2 Power."
        self.has_ongoing = True
    
    def applyOngoing(self, locationlist):
        location = self.location.returnRightOrLeftLocation(1)
        if location != None:
            location.ongoing_to_apply.append(self)
        location = self.location.returnRightOrLeftLocation(-1)
        if location != None:
            location.ongoing_to_apply.append(self)
    
    def ongoing(self, location):
        if self.ally:
            location.allies_power_buff_sum += 2
        else:
            location.enemies_power_buff_sum += 2
