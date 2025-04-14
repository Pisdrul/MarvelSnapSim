from cards import Card, copy

class Moongirl(Card):
    def __init__(self, ally, status):
        super().__init__(4, 5, "Moongirl", ally, status)
        self.description = "On Reveal: Duplicate your hand."
    
    def onReveal(self, locationlist):
        temparray = []
        if self.ally:
            for card in self.status["allyhand"]:
                temparray.append(copy.deepcopy(card))
            self.status["allyhand"]+= temparray
        else:
            for card in self.status["enemyhand"]:
                temparray.append(copy.deepcopy(card))
            self.status["enemyhand"]+= temparray