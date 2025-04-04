class Location:
    def __init__(self,number, status,locationlist):
        self.allies = []
        self.enemies = []
        self.preRevealAllies = []
        self.preRevealEnemies = []
        self.alliesPower = 0
        self.enemiesPower = 0
        self.alliesPowerBuff = 0
        self.enemiesPowerBuff = 0
        self.locationNum = number
        self.status = status
        self.locationlist = locationlist
        self.name = "Location " + str(self.locationNum)
        self.can_activate_onreveal = True
        self.can_destroy = True
        self.can_play_cards = True
        self.winning = "Tie"
        self.ongoing_number = 1
        self.on_reveal_number = 1
        self.ongoing_to_apply = []
    
    def returnRightOrLeftLocation(self, rightOrLeft):
        locations = list(self.locationlist.items())
        for i, (key, loc) in enumerate(locations):
            if loc.locationNum == self.locationNum and rightOrLeft + loc.locationNum >0 and rightOrLeft + loc.locationNum < 4:
                return locations[i + rightOrLeft][1]


    def __repr__(self):
        return f"Location {self.locationNum}"

    def addToAllies(self,unit):
        print("Adding allies!")
        if (len(self.allies) + len(self.preRevealAllies))<4:
            self.preRevealAllies.append(unit)
            return True
        else:
            print("location full")
            return False
        
    def addToEnemies(self,unit):
        print("Adding enemies!")
        if (len(self.enemies) + len(self.preRevealEnemies))<4 and self.can_play_cards:
            self.preRevealEnemies.append(unit)
            return True
        else:
            if self.can_play_cards == False:
                print("Can't play cards")
            else:
                print("location full")
            return False
        
    def countPower(self):
        power = 0
        for unit in self.allies:
            power += unit.cur_power
        self.alliesPower = power
        #check power from ongoing here
        power =0
        for unit in self.enemies:
            print(unit.name, unit.cur_power)
            power += unit.cur_power
        self.enemiesPower = power

    def handleReveals(self,unitList):
        for unit in unitList:
            if self.can_activate_onreveal:
                for i in range(self.on_reveal_number+1):
                    unit.onReveal(self.locationlist)
            if(unit.ally):
                self.allies.append(unit)
            else:
                self.enemies.append(unit)
            self.onPlayEffect(unit)
            self.updateCards()

    def revealCards(self): #bisogna fare in modo che vengano rivelate prima tutte le carte del player con prio invece che location per location
        if(self.status["allypriority"]):
            if len(self.preRevealAllies)>0:
                print("Allies are revealing on location ",self.locationNum,":", self.preRevealAllies)
                self.handleReveals(self.preRevealAllies)           
        else:
            if len(self.preRevealEnemies)>0:
                print("Enemies are revealing: on location ",self.locationNum,":", self.preRevealEnemies)
                self.handleReveals(self.preRevealEnemies)
        self.countPower()

    def locationStatus(self):
        stringA = ""
        stringB = ""
        for unit in self.allies:
            stringA += "[" + str(unit.name) + ": "+ str(unit.cur_power) + "]"
        for unit in self.enemies:
            stringB += "[" + str(unit.name) + ": "+ str(unit.cur_power) + "]"
        status = stringA + " power: "+ str(self.alliesPower) + " vs " + stringB + " power: " + str(self.enemiesPower)
        return status
    
    def updateCards(self):
        units = self.locationlist["location1"].allies + self.locationlist["location2"].allies + self.locationlist["location3"].allies+ self.locationlist["location1"].enemies + self.locationlist["location2"].enemies + self.locationlist["location3"].enemies
        for unit in units:
            if unit.has_ongoing:
                for i in range(self.ongoing_number):
                    unit.applyOngoing(self.locationlist)
        for unit in units:
            unit.updateCard()


    def undoActions(self, allyTurn):
        tempArray =[]
        if(allyTurn):
            tempArray = self.preRevealAllies
            self.preRevealAllies=[]
        else:
            tempArray = self.preRevealEnemies
            self.preRevealEnemies =[]
        return tempArray
    
    def endOfTurn(self):
        self.locationWinner()
        print("End of turn ", self.status["turncounter"])
        print("End of turn of cards in location ", self.locationNum)
        self.activateEndOfTurns(self.allies)
        self.activateEndOfTurns(self.enemies)
        #self.updateStatus()
        self.countPower()
        self.locationWinner()
        self.preRevealAllies = []
        self.preRevealEnemies = []

    def locationWinner(self):
        if self.alliesPower > self.enemiesPower:
            self.winning = "Ally"
        elif self.alliesPower < self.enemiesPower:
            self.winning = "Enemy"
        else:
            self.winning = "Tie"

    #def updateStatus(self):
    #    self.checkOngoing()

    def activateEndOfTurns(self,unitList):
        for unit in unitList:
            unit.endOfTurn()
        self.preRevealAllies,self.preRevealEnemies = [],[]
    
    def removeCard(self, card):
        if card.ally:
            self.allies.remove(card)
        else:
            self.enemies.remove(card)
    
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
        if card.can_be_destroyed and self.can_destroy:
            if card.ally:
                self.allies.remove(card)
                card.activateOnDestroy()
                self.status["alliesdestroyed"].append(card)
            else:
                self.enemies.remove(card)
                card.activateOnDestroy()
                self.status["enemiesdestroyed"].append(card)
        else:
            print(card.name," can't be destroyed!")

    def onCardBeingMovedHere(self, card):
        pass

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
