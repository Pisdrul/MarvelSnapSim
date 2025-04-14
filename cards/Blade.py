from cards import Card

class Blade(Card):
    def __init__(self, ally, status):
        super().__init__(1, 3, "Blade", ally, status)
        self.description = "On Reveal: Discard the leftmost card in your hand"
    
    def onReveal(self, locationlist):
        if self.ally:
            self.status["allyhand"][-1].discard()
        else:
            self.status["enemyhand"][-1].discard()