from cards import Card, random, copy

class Mantis(Card):
    def __init__(self, ally, status):
        super().__init__(1, 2, "Mantis", ally, status)
        self.description = "On Reveal: If your opponent played any cards here this turn, copy one of them into your hand."

    def onReveal(self, locationlist):
        if self.ally:
            if len(self.location.preRevealEnemies) >0:
                self.status["allyhand"].append(copy.deepcopy(random.choice(self.location.preRevealEnemies)))
        else:
            if len(self.location.preRevealAllies) >0:
                self.status["enemyhand"].append(copy.deepcopy(random.choice(self.location.preRevealAllies)))
