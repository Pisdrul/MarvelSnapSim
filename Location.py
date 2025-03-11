class Location:
    allies = []
    enemies = []
    preRevealAllies = []
    preRevealEnemies = []
    alliesPower = 0
    enemiesPower = 0
    def __init__(self):
        pass

    def __repr__(self):
        print()
    def countPower(self):
        for unitA in self.allies:
            self.alliesPower += self.alliesPower + unitA.power
    def addToAllies(self,unit):
        if (len(self.allies)+1)<4:
            self.preRevealAllies.append(unit)
        else:
            print("location full")
            return False
        
    def addToEnemies(self,unit):
        if (len(self.enemies)+1)<4:
            self.preRevealEnemies.append(unit)
        else:
            print("location full")
            return False
    
    def revealCards(self, allyPrio):
        if(allyPrio):
            print("Allies are revealing: ", self.preRevealAllies)
            print("Enemies are revealing: ", self.preRevealEnemies)
        else:
            print("Allies are revealing: ", self.preRevealAllies)
            print("Enemies are revealing: ", self.preRevealEnemies)
        self.allies = self.allies.concat(self.preRevealAllies)
        self.enemies = self.enemies.concat(self.preRevealEnemies)