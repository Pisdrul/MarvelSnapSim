from cards import Card

class Swarm(Card):
    def __init__(self, ally, status):
        super().__init__(2, 3, "Swarm", ally, status)
        self.description = "When discarded, add 2 copies here that cost 0"
    
    def whenDiscarded(self):
        if self.ally:
            self.status["allyhand"].append(self.createCopy())
            self.status["allyhand"].append(self.createCopy())
        else:
            self.status["enemyhand"].append(self.createCopy())
            self.status["enemyhand"].append(self.createCopy())
    
    def createCopy(self):
        zerocostcopy = Swarm(self.ally, self.status)
        zerocostcopy.cost = 0
        zerocostcopy.base_power = self.base_power
        zerocostcopy.onreveal_buff = self.onreveal_buff
        zerocostcopy.was_created = True
        return zerocostcopy
