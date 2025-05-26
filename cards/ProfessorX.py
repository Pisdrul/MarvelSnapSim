from cards import Card

class Professorx(Card):
    def __init__(self, ally, status):
        super().__init__(5, 3, "Professor X", ally, status)
        self.description = "Ongoing: Moving is the only way to add or remove a card from here."
        self.has_ongoing = True
    
    def ongoing(self, location):
        location.can_play_cards_allies, location.can_play_cards_enemies = False, False
        location.can_destroy = False
    
    def applyOngoing(self, locationlist):
        self.location.ongoing_to_apply.append(self)