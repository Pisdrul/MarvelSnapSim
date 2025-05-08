from cards import Card

class Blade(Card):
    def __init__(self, ally, status):
        super().__init__(1, 3, "Blade", ally, status)
        self.description = "On Reveal: Discard the rightmost card in your hand"
        self.moves_number = 10
    
    def onReveal(self, locationlist):
        if self.ally and len(self.status["allyhand"]) > 0:
            self.status["allyhand"][-1].discard()
        elif not self.ally and len(self.status["enemyhand"]) > 0:
            self.status["enemyhand"][-1].discard()