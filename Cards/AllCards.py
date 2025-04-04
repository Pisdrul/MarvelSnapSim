from Cards.Card import Card
from Locations.AllLocations import *
import copy
import random
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
            self.onreveal_buff += self.status["allyenergy"]
        else:
            self.onreveal_buff += self.status["enemyenergy"]

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
            self.status["allydeck"][-1].onreveal_buff += 2
        else:
            self.status["enemydeck"][-1].onreveal_buff += 2
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
        super().updateCard()
        self.cost = 12 - len(self.status["alliesdestroyed"]) - len(self.status["enemiesdestroyed"])

class Knull(Card): #Fixare Knull, ritorna NoneType quando calcola il potere della location
    def __init__(self, ally, status):
        super().__init__(1, 0, "Knull", ally, status)
        self.has_ongoing_buffpower = True
        self.description = "Ongoing: Has the combined attack of all destroyed cards"
    
    def ongoing(self, card, temppower):
        for unit in self.status["alliesdestroyed"] + self.status["enemiesdestroyed"]:
            print("Adding ", unit.power," to Knull")
            self.ongoing_buff += unit.power
    
    def toApply(self):
        self.ongoing_to_apply.append(self)

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
                self.onreveal_buff += 4
        else:
            if len(self.location.preRevealAllies) >0:
                self.onreveal_buff += 4

class Medusa(Card):
    def __init__(self, ally, status):
        super().__init__(2, 2, "Medusa", ally, status)
        self.description = "On Reveal: If this is at the middle location, +3 Power"
    
    def onReveal(self, locationlist):
        if self.location == locationlist["location2"]:
            self.onreveal_buff += 3

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
            self.onreveal_buff += 2*(len(self.location.allies))
        else:
            self.onreveal_buff += 2*(len(self.location.enemies))

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
        self.has_ongoing = True
        self.has_ongoing_buffpower = True

    def ongoing(self, card):
        card.ongoing_buff += 1
    
    def applyOngoing(self,locationlist):
        if self.ally:
            for unit in self.location.allies:
                if unit != self:
                    unit.ongoing_to_apply.append(self)
        else:
            for unit in self.location.enemies:
                if unit != self:
                    unit.ongoing_to_apply.append(self)

class Armor(Card): #Da implementare appena finisco la lista degli ongoing delle location
    def __init__(self, ally, status):
        super().__init__(2, 3, "Armor", ally, status)
        self.description("Ongoing: Cards can't be destroyed here")

class Kazan(Card):
    def __init__(self, ally, status):
        super().__init__(4, 4, "Kazan", ally, status)
        self.description = "Ongoing: Your 1-cost cards have +1 Power."
        self.has_ongoing = True

    def ongoing(self, card):
        card.ongoing_buff += 1
    
    def applyOngoing(self, locationlist):
        if self.ally:
            for unit in locationlist["location1"].allies + locationlist["location2"].allies + locationlist["location3"].allies:
                print(unit.cost)
                if unit.cost == 1:
                    unit.ongoing_to_apply.append(self)
        else:
            for unit in locationlist["location1"].enemies + locationlist["location2"].enemies + locationlist["location3"].enemies:
                if unit.cost == 1:
                    unit.ongoing_to_apply.append(self)
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
                unit.onreveal_buff += 3
        else:
            for unit in self.status["enemyhand"]:
                unit.onreveal_buff += 3

class OldCaptainAmerica(Card):
    def __init__(self, ally, status):
        super().__init__(3, 4, "Old Captain America", ally, status)
        self.description = "Ongoing: Your other cards here have +1 Power."
        self.has_ongoing = True
        self.has_ongoing_buffpower = True

    def ongoing(self, card):
        card.ongoing_buff += 1
    
    def applyOngoing(self, locationlist):
        if self.ally:
            for unit in self.location.allies:
                if unit != self:
                    unit.ongoing_to_apply.append(self)
        else:
            for unit in self.location.enemies:
                if unit != self:
                    unit.ongoing_to_apply.append(self)

class Klaw(Card):
    def __init__(self, ally, status):
        super().__init__(1, 4, "Klaw", ally, status)
        self.description = "Ongoing: The location to the right has +7 Power."
        self.has_ongoing = True

    def ongoing(self, location):
        if self.ally:
            location.allies_power_buff_sum += 7
        else:
            location.enemies_power_buff_sum += 7
    
    def applyOngoing(self, locationlist):
        location = self.location.returnRightOrLeftLocation(1)
        if location != None:
            location.ongoing_to_apply.append(self)
            print(location.ongoing_to_apply)
    