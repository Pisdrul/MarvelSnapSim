from cards import Card
import random

class Hulkbuster(Card): #carta al momento molto buggata, come per morph. potrebbe avere delle interazioni non volute 
    def __init__(self, ally, status):
        super().__init__(2, 3, "Hulk Buster", ally, status)
        self.description = "On Reveal: Merge with one of your cards here."
        self.wasmerged = False 
    
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
        if self.ally and self.wasmerged == False:
            print(self.location.preRevealAllies)
            print("up is pre reveal, down is allies")
            print(self.location.allies)
            if self in self.location.preRevealAllies: self.location.preRevealAllies.remove(self)
            self.wasmerged = True
        elif not self.ally and self.wasmerged == False:
            print(self.location.preRevealEnemies)
            print("up is pre reveal, down is enemies")
            print(self.location.enemies)
            if self in self.location.preRevealEnemies: self.location.preRevealEnemies.remove(self)