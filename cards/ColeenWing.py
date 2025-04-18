from cards import Card
import random

class Coleenwing(Card):
    def __init__(self, ally, status):
        super().__init__(2, 4, "Coleen Wing", ally, status)
        self.description = "On Reveal: Discard the lowest cost card in your hand"
    
    def onReveal(self, locationlist):
        if self.ally:
            handToCheck = self.status["allyhand"]
        else:
            handToCheck = self.status["enemyhand"]
        
        lowestCost = 100
        lowestCostCard = []
        for card in handToCheck:
            if card.cur_cost == lowestCost:
                lowestCostCard.append(card)
            if card.cur_cost < lowestCost:
                lowestCost = card.cur_cost
                lowestCostCard = [card]
        
        random.choice(lowestCostCard).discard()