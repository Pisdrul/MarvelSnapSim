from Location import *
import random

class Card:
    def __init__(self, cost, power, name, ally, status):
        self.cost = cost
        self.power = power
        self.name = name
        self.location = 0
        self.ally = ally
        self.cur_power = power
        self.has_ongoing = False
        self.status = status
        self.activate_while_in_hand = False
        
    def __repr__(self):
        return f"{self.cur_power}"
    
    def onReveal(self,locationlist):
        print("Revealed ",self.name)
    
    def playCard(self,location):
        self.location= location

    def endOfTurn(self):
        pass

    def checkOngoing(self):
        self.location.checkOngoing(self)

    def setCurPower(self, num):
        self.cur_power = num
    
    def activateOnDestroy(self):
        print("Destroyed ", self.name)




class TestCard(Card):
    def __init__(self, cost, power, name, ally, status):
        super().__init__(cost, power, name, ally, status)
    def onReveal(self,locationlist):
        print("Revealing TestCard")
        print("Current power: ", self.power)
        self.power+=2
        print("Increased power to: ", self.power)
    
class EndOfTurnTest(Card):
    def __init__(self, cost, power, name, ally, status):
        super().__init__(cost, power, name, ally, status)
        self.counter =0
    def endOfTurn(self):
        print("increasing power of", self.name)
        self.power +=1
        self.counter +=1
        if self.counter >3:
            print(self.name," destroyed itself!")
            self.location.removeCard(self)
class OngoingTest(Card):
    def __init__(self, cost, power, name, ally, status):
        super().__init__(cost, power, name, ally, status)
        self.has_ongoing = True

    def ongoing(self,power):
        print('here')
        return power * 2

class Magik(Card):
    def __init__(self, ally, status):
        super().__init__(3, 2, "Magik", ally, status)
    
    def onReveal(self,locationlist):
        if self.status["turncounter"] <=5:
            newloc = Limbo(0,self.status, locationlist)
            self.location.changeLocation(newloc)

        else:
            print("doesnt work after turn 5!")

class Sunspot(Card):
    def __init__(self, ally, status):
        super().__init__(1,0, "Sunspot", ally, status)
    def endOfTurn(self):
        if self.ally:
            self.power += self.status["allyenergy"]
        else:
            self.power += self.status["enemyenergy"]

class Psylocke(Card):
    def __init__(self, ally, status):
        super().__init__(2,1, "Psylocke", ally, status)
    
    def onReveal(self, locationlist):
        if self.ally:
            self.status["tempenergyally"] +=1
        else:
            self.status["tempenergyenemy"] +=1
        print("+1 energy next turn!")

class AmericaChavez(Card):
    def __init__(self, ally, status):
        super().__init__(1,2, "America Chavez", ally, status)
    
    def onReveal(self, locationlist):
        if self.ally:
            self.status["allydeck"][-1].power += 2
        else:
            self.status["enemydeck"][-1].power += 2
        print("Increased power of the card on top of the deck by 2!")

class Elektra(Card):
    def __init__(self, ally, status):
        super().__init__(1, 2, "Elektra", ally, status)
    
    def onReveal(self, locationlist):
        if self.ally:
            if len(self.location.enemies)>0:
                candidates = []
                for unit in self.location.enemies:
                    if unit.cost == 1:
                        candidates.append(unit)
                print(len(candidates))
                if len(candidates)==0:
                    print("No candidates!")
                else:
                    tobedestroyed = random.choice(candidates)
                    self.location.destroyCard(tobedestroyed)
        else:
            if len(self.location.allies)>0:
                candidates = []
                for unit in self.location.allies:
                    if unit.cost == 1:
                        candidates.append(unit)
                if len(candidates)==0:
                    print("No candidates!")
                else:
                    tobedestroyed = random.choose(candidates)
                    self.location.destroyCard(tobedestroyed)
