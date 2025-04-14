from cards import Card

class Apocalypse(Card):
    def __init__(self, ally, status):
        super().__init__(6, 7, "Apocalypse", ally, status)
        self.description = "When discarded, put it back with +4 power"
    
    def whenDiscarded(self):
        if self.ally:
            self.status["allyhand"].append(self)
            self.onreveal_buff += 4
        else:
            self.status["enemyhand"].append(self)
            self.onreveal_buff += 4