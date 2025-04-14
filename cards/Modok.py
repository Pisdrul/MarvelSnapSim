from cards import Card
import copy
class Modok(Card):
    def __init__(self, ally, status):
        super().__init__(5, 7, "Modok", ally, status)
        self.description = "On Reveal: Discard all cards in your hand"
    
    def onReveal(self, locationlist):
        if self.ally:
            toDiscard = copy.copy(self.status["allyhand"])
            for card in toDiscard:
                card.discard()
        else:
            toDiscard = copy.copy(self.status["enemyhand"])
            for card in toDiscard:
                card.discard()