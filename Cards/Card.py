from Location import *
import random
import copy

class Card:
    def __init__(self, cost, power, name, ally, status):
        self.cost = cost
        self.power = power
        self.name = name
        self.location = 0
        self.ally = ally
        self.cur_power = power
        self.has_ongoing = False
        self.has_ongoing_buff = False
        self.status = status
        self.activate_while_in_hand = False
        self.description = "Does nothing"
        self.can_be_destroyed = True
        self.has_ongoing_late = False
        self.ongoing_buff = False
        self.has_ongoing_buffpower = False
        self.can_move = 0 

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

    def updateCard(self):
        pass

    def ongoing(self, locationlist):
        pass
    
    def onMove(self):
        pass
    def move(self, newloc):
        if self.ally:
            next = newloc.allies
        else: 
            next = newloc.enemies
        
        if len(next)<4 and newloc != self.location:
            self.location.removeCard(self)
            self.location = newloc
            self.onMove()
            next.append(self)
            for unit in self.location.allies + self.location.enemies:
                unit.onCardBeingMovedHere()
    
    def onCardBeingMovedHere(self):
        pass




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
        self.description = "At the end of the turn, gain power equals to the amount of your unspent energy this turn"
    def endOfTurn(self):
        if self.ally:
            self.cur_power += self.status["allyenergy"]
        else:
            self.cur_power += self.status["enemyenergy"]

class Psylocke(Card):
    def __init__(self, ally, status):
        super().__init__(2,1, "Psylocke", ally, status)
        self.description = "On reveal: +1 energy next turn"
    
    def onReveal(self, locationlist):
        if self.ally:
            self.status["tempenergyally"] +=1
        else:
            self.status["tempenergyenemy"] +=1
        print("+1 energy next turn!")

class AmericaChavez(Card):
    def __init__(self, ally, status):
        super().__init__(1,2, "America Chavez", ally, status)
        self.description = "On Reveal: Give the top card of your deck +2 power"
    
    def onReveal(self, locationlist):
        if self.ally:
            self.status["allydeck"][-1].power += 2
        else:
            self.status["enemydeck"][-1].power += 2
        print("Increased power of the card on top of the deck by 2!")

class Elektra(Card):
    def __init__(self, ally, status):
        super().__init__(1, 2, "Elektra", ally, status)
        self.description = "On Reveal: Replace this location with Limbo. Does not work after turn 5"
    
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
                    tobedestroyed = random.choice(candidates)
                    self.location.destroyCard(tobedestroyed)

class Death(Card):
    def __init__(self, ally, status):
        super().__init__(8, 12, "Death", ally, status)
        self.description = "Costs 1 less for each card that was destroyed this game"
    
    def updateCard(self):
        self.cost = 12 - len(self.status["alliesdestroyed"]) - len(self.status["enemiesdestroyed"])

class Knull(Card): #Fixare Knull, ritorna NoneType quando calcola il potere della location
    def __init__(self, ally, status):
        super().__init__(1, 0, "Knull", ally, status)
        self.has_ongoing_buffpower = True
        self.description = "Ongoing: Has the combined attack of all destroyed cards"
    
    def ongoing(self, card,temppower):
        for unit in self.status["alliesdestroyed"] + self.status["enemiesdestroyed"]:
            print("Adding ", unit.power," to Knull")
            self.cur_power += unit.power

class Sentinel(Card):
    def __init__(self, ally, status):
        super().__init__(2, 3, "Sentinel", ally, status)
        self.description = "On Reveal: Add another Sentinel card to your hand"

    def onReveal(self, locationlist):
        if self.ally:
            self.status["allyhand"].append(Sentinel(self.ally, self.status))
        else:
            self.status["enemyhand"].append(Sentinel(self.ally, self.status))
        
        print("Added another Sentinel card to your hand")

class StarLord(Card):
    def __init__(self, ally, status):
        super().__init__(2, 2, "Star Lord", ally, status)
        self.description = "On Reveal: If your opponent played a card here this turn, +4 power."

    def onReveal(self, locationlist):
        if self.ally:
            if len(self.location.preRevealEnemies) >0:
                self.cur_power += 4
        else:
            if len(self.location.preRevealAllies) >0:
                self.cur_power += 4

class Medusa(Card):
    def __init__(self, ally, status):
        super().__init__(2, 2, "Medusa", ally, status)
        self.description = "On Reveal: If this is at the middle location, +3 Power"
    
    def onReveal(self, locationlist):
        if self.location == locationlist["location2"]:
            self.cur_power += 3

class Odin(Card):
    def __init__(self, ally, status):
        super().__init__(6, 8, "Odin", ally, status)
        self.description = "On Reveal: Repeat the On Reveal abilities of your other cards here"
    
    def onReveal(self, locationlist):
        if self.ally:
            cur = self.location.allies
        else:
            cur = self.location.enemies
        for unit in cur:
            if unit != self:
                unit.onReveal(locationlist)

class Wolfsbane(Card):
    def __init__(self, ally, status):
        super().__init__(3, 1, "Wolfsbane", ally, status)
        self.description = "On Reveal: +2 Power for each other card you have here"
    
    def onReveal(self, locationlist):
        if self.ally: 
            self.cur_power += 2*(len(self.location.allies))
        else:
            self.cur_powerpower += 2*(len(self.location.enemies))

class WhiteTiger(Card):
    def __init__(self, ally, status):
        super().__init__(5, 1, "White Tiger", ally, status)
        self.description = "On Reveal: Add a 8-Power Tiger to another location."
    
    def onReveal(self, locationlist):
        possible = []
        if self.ally:
            for loc in locationlist.values():
                if loc != self.location and len(loc.allies) <4:
                        possible.append(loc)
        else:
            for loc in locationlist.values():
                if loc != self.location and len(loc.enemies) <4:
                        possible.append[loc]
        if len(possible) > 0:
            loc = random.choice(possible)
            loc.allies.append(Card(5, 8, "Tiger", self.ally, self.status))
        else:
            print("No possible locations")

class Ironman(Card):
    def __init__(self, ally, status):
        super().__init__(5, 0, "Ironman", ally, status)
        self.description = "Ongoing = Your total Power is doubled here."
        self.has_ongoing_late = True
    
    def ongoing(self, locationlist):
        if self.ally:
            self.location.alliesPowerWithBuff = self.location.alliesPowerWithBuff * 2
        else:
            self.location.enemiesPowerWithBuff = self.location.enemiesPowerWithBuff * 2

class CaptainAmerica(Card):
    def __init__(self, ally, status):
        super().__init__(3, 3, "Captain America", ally, status)
        self.description = "Ongoing: Your other Ongoing cards here have +2 Power."
        self.has_ongoing_buffpower = True
    
    def ongoing(self, locationlist):
        if self.ally:
            for unit in self.location.allies:
                if unit.has_ongoing:
                    unit.ongoing_buff += 2
        else:
            for unit in self.location.enemies:
                if unit.has_ongoing:
                    unit.ongoing_buff += 2

class Heimdall(Card):
    def __init__(self, ally, status):
        super().__init__(1, 10, "Heimdall", ally, status)
        self.description = "On Reveal: Move your other cards one location to the left"

    def onReveal(self, locationlist):
        print("Heimdall!")
        if self.ally:
            for unit in locationlist["location1"].allies + locationlist["location2"].allies + locationlist["location3"].allies:
                if unit != self:
                    newloc= unit.location.returnRightOrLeftLocation(-1)
                    if newloc != None:
                        unit.move(unit.location.returnRightOrLeftLocation(-1))
        else:
            for unit in locationlist["location1"].enemies + locationlist["location2"].enemies + locationlist["location3"].enemies:
                if unit != self:
                    newloc= unit.location.returnRightOrLeftLocation(-1)
                    if newloc != None:
                        unit.move(unit.location.returnRightOrLeftLocation(-1))

class MultipleMan(Card):
    def __init__(self, ally, status):
        super().__init__(2, 3, "Multiple Man", ally, status)
        self.description = "When this moves, add a copy to the old location"

    def move(self, newloc):
        if self.ally:
            cur = self.location.allies
            next = newloc.allies
        else: 
            cur = self.location.enemies
            next = newloc.enemies
        if len(next)<4 and newloc != self.location:
            self.location.removeCard(self)
            self.location = newloc
            cur.append(copy.deepcopy(self))
            next.append(self)
            for unit in self.location.allies + self.location.enemies:
                unit.onCardBeingMovedHere()
    
class HandBuffTest(Card):
    def __init__(self, ally, status):
        super().__init__(0, 0, "HandBuffTest", ally, status)
        self.description = "On Reveal: Give +3 power to every card in your hand"
    
    def onReveal(self, locationlist):
        if self.ally:
            for unit in self.status["allyhand"]:
                unit.cur_power += 3
        else:
            for unit in self.status["enemyhand"]:
                unit.cur_power += 3