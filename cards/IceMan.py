from cards import Card
import random

class Iceman(Card):
    def __init__(self, ally, status):
        super().__init__(1, 2, "Iceman", ally, status)
        self.description = "On Reveal: Give a card in your opponent’s hand +1 Cost. (maximum 6)"
    
    def onReveal(self, locationlist):
        toDebuff = []
        if self.ally:
            if len(self.status["enemyhand"]) > 0:
                for card in self.status["enemyhand"]:
                    if card.cost < 6:
                        toDebuff.append(card)
        else:
            if len(self.status["allyhand"]) > 0:
                for card in self.status["allyhand"]:
                    if card.cost < 6:
                        toDebuff.append(card)
        if len(toDebuff) > 0:
            choice = random.choice(toDebuff)
            choice.cost += 1
            print(f"{choice.name}", "now has a cost of", choice.cost)