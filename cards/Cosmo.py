from cards import Card

class Cosmo(Card):
    def __init__(self, ally, status):
        super().__init__(3, 3, "Cosmo", ally, status)
        self.description = "Ongoing: On Reveal abilities won't happen here"
        self.has_ongoing = True
    
    def applyOngoing(self, locationlist):
        self.location.ongoing_to_apply.append(self)
    
    def ongoing(self, location):
        location.on_reveal_number_allies, location.on_reveal_number_enemies = 0, 0