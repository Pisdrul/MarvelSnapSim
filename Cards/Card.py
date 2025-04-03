from Locations.Location import Location
from Locations.AllLocations import *
import random
import copy

class Card:
    def __init__(self, cost, power, name, ally, status):
        self.cost = cost
        self.base_power = power
        self.name = name
        self.location = 0
        self.ally = ally
        self.cur_power = self.base_power
        self.onreveal_buff = 0 
        self.has_ongoing = False
        self.has_ongoing_buff = False
        self.status = status
        self.activate_while_in_hand = False
        self.description = "Does nothing"
        self.can_be_destroyed = True
        self.has_ongoing_late = False
        self.ongoing_buff = 0
        self.ongoing_to_apply = []
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

    def setPower(self, num):
        set.base_power = num
    
    def activateOnDestroy(self):
        print("Destroyed ", self.name)

    def updateCard(self):
        self.canbedestroyed = True
        self.ongoing_buff = 0
        for buff in self.ongoing_to_apply:
            buff.ongoing(self)
        self.cur_power = self.base_power + self.onreveal_buff + self.ongoing_buff
        self.ongoing_to_apply = []

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




