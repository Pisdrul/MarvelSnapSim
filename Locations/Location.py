import random, inspect, sys
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
        self.can_destroy_base = True
        self.can_play_cards_base = True
        self.can_play_cards_allies = self.can_play_cards_base
        self.can_play_cards_enemies = self.can_play_cards_base
        self.winning = "Tie"
        self.ongoing_number_base = 1
        self.ongoing_number_allies = self.ongoing_number_base
        self.ongoing_number_enemies = self.ongoing_number_base
        self.on_reveal_number_base = 1
        self.on_reveal_number_allies = self.on_reveal_number_base
        self.on_reveal_number_enemies = self.on_reveal_number_base
        self.ongoing_to_apply = []
        self.onslaught_number = []
        self.allies_power_buff_sum = 0
        self.allies_power_buff_mult = 1
        self.enemies_power_buff_sum = 0
        self.enemies_power_buff_mult = 1
        self.onslaught_allies = []
        self.onslaught_enemies = []
        self.tribunal_allies = False
        self.tribunal_enemies = False
        self.can_destroy = self.can_destroy_base
        self.location_can_be_moved_to = False
        self.cards_to_move = []
    
    def resetVariablesPreOngoing(self):
        self.ongoing_number_allies = self.ongoing_number_base
        self.ongoing_number_enemies = self.ongoing_number_base
        self.on_reveal_number_allies, self.on_reveal_number_enemies = self.on_reveal_number_base, self.on_reveal_number_base
        self.allies_power_buff_sum = 0
        self.allies_power_buff_mult = 1
        self.enemies_power_buff_sum = 0
        self.enemies_power_buff_mult = 1
        self.can_play_cards_enemies, self.can_play_cards_allies = self.can_play_cards_base, self.can_play_cards_base
        self.can_destroy = self.can_destroy_base
    def returnRightOrLeftLocation(self, rightOrLeft):
        locations = list(self.locationlist.items())
        for i, (key, loc) in enumerate(locations):
            if loc.locationNum == self.locationNum and rightOrLeft + loc.locationNum >0 and rightOrLeft + loc.locationNum < 4:
                return locations[i + rightOrLeft][1]


    def __repr__(self):
        return f"Location {self.locationNum}"

    def canCardBePlayed(self,unit):
        if unit.can_be_played:
            return True
        else:
            return False
    def addToAllies(self,unit):
        print("Adding allies!")
        if not self.checkIfLocationFull(True) and self.can_play_cards_allies:
                if self.canCardBePlayed(unit):
                    self.preRevealAllies.append(unit)
                    return True
                else:
                    print("Can't play that card here")
                    return False
        else:
            if (self.can_play_cards_allies == False): print("Can't play cards")
            else: print("location full")
            return False
        
    def addToEnemies(self,unit):
        print("Adding enemies!")
        if not self.checkIfLocationFull(unit.ally) and self.can_play_cards_enemies:
            self.preRevealEnemies.append(unit)
            return True
        else:
            if self.can_play_cards_enemies == False:
                print("Can't play cards")
            else:
                print("location full")
            return False
    
    #controlla se la location è full o meno in base a chi sta giocando controllando le carte che stanno per essere giocate + quelle già giocate e quelle che si devono muovere
    def checkIfLocationFull(self,allyOrEnemy):
        full = False
        num = 0
        if allyOrEnemy:
            num += len(self.preRevealAllies) + len(self.allies)
            if num == 4:
                full = True
                return full
        else:
            num += len(self.preRevealEnemies) + len(self.enemies)
            if num == 4:
                full = True
                return full
        for location in self.locationlist.values():
            if location != self:
                for move in location.cards_to_move:
                    if move[1] == self and move[0].ally == allyOrEnemy:
                        num += 1
                    if num == 4:
                        full = True
                        break
        return full

    def countPower(self):
        power = 0
        for unit in self.allies:
            power += unit.cur_power
        self.alliesPower = power + self.allies_power_buff_sum 
        self.alliesPower *= self.allies_power_buff_mult
        power =0
        for unit in self.enemies:
            power += unit.cur_power
        self.enemiesPower = power + self.enemies_power_buff_sum
        self.enemiesPower *= self.enemies_power_buff_mult
        
    def updateGameState(self):
        for location in self.locationlist.values():
            location.updateCards()
            location.updateLocation()

    def updateLocation(self):
        self.resetVariablesPreOngoing()
        for unit in self.ongoing_to_apply:
            unit.ongoing(self)
        self.ongoing_to_apply.clear()

    def updateCards(self):
        units = self.allies + self.enemies
        self.ongoing_number = self.ongoing_number_base
        for unit in units:
            if unit.has_ongoing:
                for i in range(self.ongoing_number):
                    unit.applyOngoing(self.locationlist)
        for unit in units:
            unit.updateCard()

    def startOfTurn(self):
        self.updateGameState()

    def handleReveals(self,unitList):
        for unit in unitList:
            if self.can_activate_onreveal:
                if unit.ally:
                    for i in range(self.on_reveal_number_allies):
                        unit.onReveal(self.locationlist)
                else:
                    for i in range(self.on_reveal_number_enemies):
                        unit.onReveal(self.locationlist)
            if(unit.ally):
                self.allies.append(unit)
            else:
                self.enemies.append(unit)
            self.onPlayEffect(unit)
            self.updateGameState()

    def startOfTurnMoves(self):
        for move in self.cards_to_move:
            move[0].move(move[1])
            if move[0].moves_number >0:
                move[0].moves_number -= 1
            self.updateGameState()
    def revealCards(self):
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

    def undoActions(self, allyTurn):
        tempArray =[]
        if(allyTurn):
            tempArray = self.preRevealAllies
            self.preRevealAllies=[]
        else:
            tempArray = self.preRevealEnemies
            self.preRevealEnemies =[]
        for move in self.cards_to_move:
                if move[0].ally == allyTurn:
                    self.cards_to_move.remove(move)
        return tempArray
    
    def endOfTurn(self):
        self.locationWinner()
        print("End of turn ", self.status["turncounter"])
        print("End of turn of cards in location ", self.locationNum)
        self.activateEndOfTurns(self.allies)
        self.activateEndOfTurns(self.enemies)
        self.updateGameState()
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

    def randomLocation(self):
        import Locations.AllLocations
        classes = [cls for name, cls in inspect.getmembers(Locations.AllLocations, inspect.isclass)
               if cls.__module__ == Locations.AllLocations.__name__]
        return random.choice(classes)(self.locationNum,self.status,self.locationlist)

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
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.counter = number
        self.newLoc = self.randomLocation()
        self.name = "Revealing location in " + str(self.counter) + " turns"
    
    def startOfTurn(self):
        super().startOfTurn()
        print(self.locationNum)
        self.counter -= 1
        if self.counter ==0: self.changeLocation(self.newLoc)
        self.name = "Revealing location in " + str(self.counter) + " turns"
