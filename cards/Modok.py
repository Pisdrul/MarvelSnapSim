from cards import Card
import copy
class Modok(Card):
    def __init__(self, ally, status):
        super().__init__(5, 7, "Modok", ally, status)
        self.description = "On Reveal: Discard all cards in your hand"
    
    def onReveal(self, locationlist):
        if self.ally and len(self.status["allyhand"]) > 0:
            toDiscard = copy.copy(self.status["allyhand"])
            for card in toDiscard:
                card.discard()
        elif not self.ally and len(self.status["enemyhand"]) > 0:
            toDiscard = copy.copy(self.status["enemyhand"])
            for card in toDiscard:
                card.discard()