from cards import Card

class Kazar(Card):
    def __init__(self, ally, status):
        super().__init__(4, 4, "Kazar", ally, status)
        self.description = "Ongoing: Your 1-cost cards have +1 Power."
        self.has_ongoing = True

    def ongoing(self, card):
        card.ongoing_buff += 1
    
    def applyOngoing(self, locationlist):
        if self.ally:
            for unit in locationlist["location1"].allies + locationlist["location2"].allies + locationlist["location3"].allies:
                if unit.base_cost == 1:
                    unit.ongoing_to_apply.append(self)
        else:
            for unit in locationlist["location1"].enemies + locationlist["location2"].enemies + locationlist["location3"].enemies:
                if unit.base_cost == 1:
                    unit.ongoing_to_apply.append(self)
