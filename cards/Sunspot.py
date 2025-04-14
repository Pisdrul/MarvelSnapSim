from cards.Card from cards import Card
class Sunspot(Card):
    def __init__(self, ally, status):
        super().__init__(1,0, "Sunspot", ally, status)
        self.description = "At the end of the turn, gain power equals to the amount of your unspent energy this turn"
    def endOfTurn(self):
        if self.ally:
            self.onreveal_buff += self.status["allyenergy"]
        else:
            self.onreveal_buff += self.status["enemyenergy"]
