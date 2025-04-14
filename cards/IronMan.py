from cards import Card
class Ironman(Card):
    def __init__(self, ally, status):
        super().__init__(5, 0, "Ironman", ally, status)
        self.description = "Ongoing = Your total Power is doubled here."
        self.has_ongoing = True
    
    def ongoing(self, locationlist):
        if self.ally:
            self.location.allies_power_buff_mult = self.location.allies_power_buff_mult * 2
        else:
            self.location.enemies_power_buff_mult = self.location.enemies_power_buff_mult * 2
    
    def applyOngoing(self, locationlist):
        self.location.ongoing_to_apply.append(self)