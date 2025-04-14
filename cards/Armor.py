from cards import Card

class Armor(Card): 
    def __init__(self, ally, status):
        super().__init__(2, 3, "Armor", ally, status)
        self.description= "Ongoing: Cards can't be destroyed here"
        self.has_ongoing = True
    
    def applyOngoing(self, locationlist):
        self.location.ongoing_to_apply.append(self)
    
    def ongoing(self, location):
        location.can_destroy = False