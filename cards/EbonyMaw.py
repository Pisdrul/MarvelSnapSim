from cards import Card

class Ebonymaw(Card):
    def __init__(self, ally, status):
        super().__init__(1, 7, "Ebony Maw", ally, status)
        self.description = "You can't play this after turn 3. Ongoing: You can't play cards here"
        self.has_ongoing = True
    
    def updateCard(self,locationlist):
        super().updateCard(locationlist)
        if self.status["turncounter"] > 3:
            self.can_be_played = False
        
    def ongoing(self, location):
        if self.ally:
            location.can_play_cards_allies = False
        else:
            location.can_play_cards_enemies = False
    
    def applyOngoing(self, locationlist):
        self.location.ongoing_to_apply.append(self)