from cards import Card

class Scorpion(Card):
    def __init__(self, ally, status):
        super().__init__(2, 2, "Scorpion", ally, status)
        self.description = "On Reveal: Afflict cards in your opponent’s hand with -1 Power."
    
    def onReveal(self, locationlist):
        if self.ally:
            for card in self.status["enemyhand"]:
                card.onreveal_buff -= 1
        else:
            for card in self.status["allyhand"]:
                card.onreveal_buff -= 1