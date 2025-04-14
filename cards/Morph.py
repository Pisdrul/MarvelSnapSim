from cards import Card,copy,random

class Morph(Card):
    def __init__(self, ally, status):
        super().__init__(3, 0, "Morph", ally, status)
        self.description = "On Reveal: Become a copy of a card in your opponent's hand"

    def onReveal(self, locationlist):
        if self.ally:
            if len(self.status["enemyhand"]) != 0:
                self.location.preRevealAllies.remove(self)
                morphInto = copy.deepcopy(random.choice(self.status["enemyhand"]))
                self.location.allies.append(morphInto)
                morphInto.location = self.location
                morphInto.ally = True
                morphInto.onReveal(locationlist)
        else:
            if len(self.status["allyhand"]) != 0:
                self.location.PreRevealEnemies.remove(self)
                morphInto = copy.deepcopy(random.choice(self.status["allyhand"]))
                self.location.enemies.append(morphInto)
                morphInto.location = self.location
                morphInto.ally = False
                morphInto.onReveal(locationlist)