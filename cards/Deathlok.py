from cards import Card
class Deathlok(Card):
    def __init__(self, ally, status):
        super().__init__(3, 5, "Deathlok", ally, status)
        self.description = "On Reveal: Destroy your other cards here"
    
    def onReveal(self, locationlist):
        if self.ally:
            for card in self.location.allies:
                if card != self:
                    self.location.destroyCard(card)
        else:
            for card in self.location.enemies:
                if card != self:
                    self.location.destroyCard(card)