from cards import Card
import copy,random

class Morph(Card): #carta al momento buggata, come per hulkbuster. potrebbe avere qualche interazione sbaglaita
    def __init__(self, ally, status):
        super().__init__(3, 0, "Morph", ally, status)
        self.description = "On Reveal: Become a copy of a card in your opponent's hand"
        self.wasmorphed = False

    def onReveal(self, locationlist):
        if self.ally and self.wasmorphed == False:
            if len(self.status["enemyhand"]) > 0:
                print("Allies:", self.location.allies)
                print("pre reveal:" , self.location.preRevealAllies)
                morphinto = random.choice(self.status["enemyhand"])
                newcard = copy.deepcopy(morphinto)
                self.location.allies.append(newcard)
                newcard.location = self.location
                newcard.ally = True
                if self in self.location.allies: self.location.allies.remove(self)
                if newcard.name != "Morph": newcard.onReveal(locationlist)
                self.wasmorphed = True
        elif not self.ally and self.wasmorphed == False:
            if len(self.status["allyhand"]) != 0:
                print("morphin time")
                print("Enemies:", self.location.enemies)
                print("pre reveal:" , self.location.preRevealEnemies)
                morphinto = random.choice(self.status["allyhand"])
                newcard = copy.deepcopy(morphinto)
                self.location.enemies.append(newcard)
                newcard.location = self.location
                newcard.ally = False
                if self in self.location.enemies: self.location.enemies.remove(self)
                if newcard.name != "Morph": newcard.onReveal(locationlist)
                self.wasmorphed = True