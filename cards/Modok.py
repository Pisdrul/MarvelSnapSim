from cards import Card
import copy
class Modok(Card):
    def __init__(self, ally, status):
        super().__init__(5, 7, "Modok", ally, status)
        self.description = "On Reveal: Discard all cards in your hand"
    
    def onReveal(self, locationlist):
        toDiscard = []
        if self.ally and len(self.status["allyhand"]) > 0:
            for card in self.status["allyhand"]:
                toDiscard.append(card)
        elif not self.ally and len(self.status["enemyhand"]) > 0:
            for card in self.status["enemyhand"]:
                toDiscard.append(card)
        for card in toDiscard:
            card.discard()
        toDiscard.clear()