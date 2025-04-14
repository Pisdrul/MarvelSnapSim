from cards import Card
class Nakia(Card):
    def __init__(self, ally, status):
        super().__init__(3, 3, "Nakia", ally, status)
        self.description = "On Reveal: Give +1 power to all cards in your hand"
    
    def onReveal(self, locationlist):
        if self.ally:
            for card in self.status["allyhand"]:
                card.onreveal_buff += 1
        else:
            for card in self.status["enemyhand"]:
                card.onreveal_buff += 1