from cards import Card

class Carnage(Card):
    def __init__(self, ally, status):
        super().__init__(2, 2, "Carnage", ally, status)
        self.description = "On Reveal: Destroy all your cards here. +2 Power for each destroyed"
    
    def onReveal(self, locationlist):
        cardsToDestroy = []
        if self.ally:
            for card in self.location.allies:
                if card != self:
                    cardsToDestroy.append(card)
        else:
            for card in self.location.enemies:
                if card != self:
                    cardsToDestroy.append(card)
        for card in cardsToDestroy:
                self.location.destroyCard(card)
                self.onreveal_buff += 2