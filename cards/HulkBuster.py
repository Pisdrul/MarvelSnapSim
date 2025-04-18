from cards import Card
import random

class Hulkbuster(Card):
    def __init__(self, ally, status):
        super().__init__(2, 3, "Hulk Buster", ally, status)
        self.description = "On Reveal: Merge with one of your cards here."
    
    def onReveal(self, locationlist):
        toMergeWith = []
        if self.ally:
            if len(self.location.allies) > 0:
                for card in self.location.allies:
                    if card != self:
                        toMergeWith.append(card)
        else:
            if len(self.location.enemies) > 0:
                for card in self.location.enemies:
                    if card != self:
                        toMergeWith.append(card)
        if len(toMergeWith) > 0:
            choice = random.choice(toMergeWith)
            self.merge(choice)
    
    def merge(self, card):
        card.onreveal_buff += self.cur_power
        if self.ally:
            self.location.allies.remove(self)
        else:
            self.location.enemies.remove(self)