from cards import Card

class Captainamerica(Card):
    def __init__(self, ally, status):
        super().__init__(3, 3, "Captain America", ally, status)
        self.description = "Ongoing: Your other Ongoing cards here have +2 Power."
        self.has_ongoing = True

    def ongoing(self, card):
        card.ongoing_buff += 2
    
    def applyOngoing(self,locationlist):
        if self.ally:
            for unit in self.location.allies:
                if unit != self:
                    unit.ongoing_to_apply.append(self)
        else:
            for unit in self.location.enemies:
                if unit != self:
                    unit.ongoing_to_apply.append(self)