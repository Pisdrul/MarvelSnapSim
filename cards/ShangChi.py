from cards import Card

class ShangChi(Card):
    def __init__(self, ally, status):
        super().__init__(4, 3, "Shang-Chi", ally, status)
        self.description = "On Reveal: Destroy all enemy cards here with 10+ Power"
    
    def onReveal(self, locationlist):
        if self.ally:
            for card in self.location.enemies:
                if card.cur_power >= 10:
                    self.location.destroyCard(card)
        else:
            for card in self.location.allies:
                if card.cur_power >= 10:
                    self.location.destroyCard(card) 