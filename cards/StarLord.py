from cards import Card
class Starlord(Card):
    def __init__(self, ally, status):
        super().__init__(2, 2, "Star Lord", ally, status)
        self.description = "On Reveal: If your opponent played a card here this turn, +4 power."

    def onReveal(self, locationlist):
        if self.ally:
            if len(self.location.preRevealEnemies) >0:
                self.onreveal_buff += 4
        else:
            if len(self.location.preRevealAllies) >0:
                self.onreveal_buff += 4