class Location:
    def __init__(self,number):
        self.allies = []
        self.enemies = []
        self.preRevealAllies = []
        self.preRevealEnemies = []
        self.alliesPower = 0
        self.enemiesPower = 0
        self.locationNum = number

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

    def activateOnReveals(self,unitList):
        for unit in unitList:
            unit.onReveal()

    def revealCards(self, allyPrio): #bisogna fare in modo che vengano rivelate prima tutte le carte del player con prio invece che location per location
        if(allyPrio):
            if len(self.preRevealAllies)>0:
                print("Allies are revealing on location ",self.locationNum,":", self.preRevealAllies)
                self.activateOnReveals(self.preRevealAllies)
                self.allies = self.allies +self.preRevealAllies
            if len(self.preRevealEnemies)>0:
                print("Enemies are revealing on location ",self.locationNum,":", self.preRevealEnemies)
                self.activateOnReveals(self.preRevealEnemies)
                self.enemies = self.enemies + self.preRevealEnemies
            
        else:
            if len(self.preRevealEnemies)>0:
                print("Enemies are revealing: on location ",self.locationNum,":", self.preRevealEnemies)
                self.activateOnReveals(self.preRevealEnemies)
                self.enemies = self.enemies + self.preRevealEnemies
            if len(self.preRevealAllies)>0:
                print("Allies are revealing on location ",self.locationNum,":", self.preRevealAllies)
                self.activateOnReveals(self.preRevealAllies)
                self.allies = self.allies +self.preRevealAllies
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