class Location:
    def __init__(self,number, status,locationlist):
        self.allies = []
        self.enemies = []
        self.preRevealAllies = []
        self.preRevealEnemies = []
        self.alliesPower = 0
        self.enemiesPower = 0
        self.locationNum = number
        self.status = status
        self.locationlist = locationlist
        self.name = "Location " + str(self.locationNum)
        self.can_activate_onreveal = True
        self.can_destroy = True
        self.can_play_cards = True
        

    def __repr__(self):
        return f"Location {self.locationNum}"

    def countPower(self):
        for unitA in self.allies:
            self.alliesPower += self.alliesPower + unitA.power

    def addToAllies(self,unit):
        print("Adding allies!")
        if (len(self.allies)+1)<4:
            self.preRevealAllies.append(unit)
        else:
            print("location full")
            return False
        
    def addToEnemies(self,unit):
        print("Adding enemies!")
        if (len(self.enemies)+1)<4:
            self.preRevealEnemies.append(unit)
        else:
            print("location full")
            return False
        
    def countPower(self):
        power = 0
        for unit in self.allies:
            power += unit.cur_power
        self.alliesPower = power
        power =0
        for unit in self.enemies:
            power += unit.cur_power
        self.enemiesPower = power

    def handleReveals(self,unitList):
        for unit in unitList:
            if self.can_activate_onreveal:
                unit.onReveal(self.locationlist)
            if(unit.ally):
                self.allies.append(unit)
            else:
                self.enemies.append(unit)
            self.onPlayEffect(unit)

    def revealCards(self, allyPrio): #bisogna fare in modo che vengano rivelate prima tutte le carte del player con prio invece che location per location
        if(allyPrio):
            if len(self.preRevealAllies)>0:
                print("Allies are revealing on location ",self.locationNum,":", self.preRevealAllies)
                self.handleReveals(self.preRevealAllies)

            if len(self.preRevealEnemies)>0:
                print("Enemies are revealing on location ",self.locationNum,":", self.preRevealEnemies)
                self.handleReveals(self.preRevealEnemies)
            
        else:
            if len(self.preRevealEnemies)>0:
                print("Enemies are revealing: on location ",self.locationNum,":", self.preRevealEnemies)
                self.handleReveals(self.preRevealEnemies)
            if len(self.preRevealAllies)>0:
                print("Allies are revealing on location ",self.locationNum,":", self.preRevealAllies)
                self.handleReveals(self.preRevealAllies)
        self.countPower()
        self.preRevealAllies, self.preRevealEnemies = [],[]

    def locationStatus(self):
        string = str(self.allies) + " power: "+ str(self.alliesPower) + " vs " + str(self.enemies) + " power: " + str(self.enemiesPower)
        return string
    
    def undoActions(self, allyTurn):
        tempArray =[]
        if(allyTurn):
            tempArray = self.preRevealAllies
            
        else:
            tempArray = self.preRevealEnemies
        return tempArray
    
    def endOfTurn(self):
        print("End of turn ", self.status["turncounter"])
        print("End of turn of cards in location ", self.locationNum)
        self.activateEndOfTurns(self.allies)
        self.activateEndOfTurns(self.enemies)
        self.updateStatus()
        self.countPower()

    def updateStatus(self):
        for unit in self.allies:
            self.checkOngoingBuffPower(unit)
        for unit in self.enemies:
            self.checkOngoingBuffPower(unit)    

    def activateEndOfTurns(self,unitList):
        print(unitList)
        for unit in unitList:
            unit.endOfTurn()
    
    def removeCard(self, card):
        if card.ally:
            self.allies.remove(card)
        else:
            self.enemies.remove(card)
    
    def checkOngoingBuffPower(self,card):
        tempPower = card.power
        print(tempPower)
        if card.ally:
            for unit in self.allies:
                print("Here for ", unit)
                if unit.has_ongoing:
                    tempPower= unit.ongoing(tempPower)
        card.setCurPower(tempPower)
    
    def onPlayEffect(self,card):
        print("Activated on play effect of location!")
    
    def onRevealLocation(self):
        print("Revealed location")
    
    def changeLocation(self, newLocation):
        newLocation.allies, newLocation.preRevealAllies = self.allies, self.preRevealAllies
        newLocation.enemies, newLocation.preRevealEnemies = self.enemies, self.preRevealEnemies
        newLocation.locationNum = self.locationNum
        temp = "location" + str(self.locationNum)
        self.locationlist[temp] = newLocation
        newLocation.onRevealLocation()
    
    def destroyCard(self, card):
        if card.ally:
            self.allies.remove(card)
            card.activateOnDestroy()
            self.status["alliesdestroyed"].append(card)
        else:
            self.enemies.remove(card)
            card.activateOnDestroy()
            self.status["enemiesdestroyed"].append(card)

class TestLocationEffects(Location):
    def __init__(self,number, status,locationlist):
        super().__init__(number,status,locationlist)
        self.counter = 0
        self.name = "On play effect test"
    
    def onPlayEffect(self, card):
        self.counter += 1
        if self.counter == 3:
            print("Destroyed ", card.name)
            self.removeCard(card)
            self.counter =0

class onRevealActivatesTwice(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Double on reveals"
    def handleReveals(self, unitList):
         for unit in unitList:
            print("Activating ", unit.name, " twice!")
            unit.onReveal(self.locationlist)
            unit.onReveal(self.locationlist)
            if(unit.ally):
                self.allies.append(unit)
            else:
                self.enemies.append(unit)
            self.onPlayEffect(unit)

class Limbo(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Limbo"
    def onRevealLocation(self):
        self.status["maxturns"] = 7
    def changeLocation(self, newLocation):
        super().changeLocation(newLocation)
        check = False
        for key, location in self.locationlist:
            if location.name == "Limbo":
                check = True
        if not check:
            self.status["maxturns"] = 6

class TemporaryLocation(Location):
    def __init__(self, number, status, locationlist, newLoc):
        super().__init__(number, status, locationlist)
        self.counter = number - 1
        self.newLoc = newLoc
        self.name = "Revealing location in " + str(self.counter) + " turns"
    
    def endOfTurn(self):
        self.counter -= 1
        if self.counter ==0: self.changeLocation(self.newLoc)
        self.name = "Revealing location in " + str(self.counter) + " turns"