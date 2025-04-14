from cards import Card

class Enchantress(Card):
    def __init__(self, ally, status):
        super().__init__(4, 6, "Enchantress", ally, status)
        self.description = "On Reveal: Remove the abilities from all Ongoing cards here"
    
    def onReveal(self, locationlist):
        if self.ally:
            for unit in self.location.enemies:
                unit.has_ongoing = False
        else:
            for unit in self.location.allies:
                unit.has_ongoing = False