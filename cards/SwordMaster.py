from cards import Card
import random

class Swordmaster(Card):
    def __init__(self, ally, status):
        super().__init__(3, 6, "Sword Master", ally, status)
        self.description = "On Reveal: Discard an odd-costed card from your hand."
    
    def onReveal(self, locationlist):
        toChoose = []
        if self.ally:
            for card in self.status["allyhand"]:
                if card.cur_cost % 2 == 1 and card != self:
                    toChoose.append(card)
        else:
            for card in self.status["enemyhand"]:
                if card.cur_cost % 2 == 1 and card != self:
                    toChoose.append(card)
        if len(toChoose) > 0:
            random.choice(toChoose).discard()