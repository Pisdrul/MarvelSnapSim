from Locations.Location import Location
import random
import copy

class Wakanda(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Wakanda"
        self.description = "Cards here can't be destroyed"
        self.can_destroy_base = False

class BarWithNoName(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Bar with no name"
        self.description = "Whoever has the least Power here wins."

    def locationWinner(self):
        if self.alliesPower < self.enemiesPower:
            self.winning = "Ally"
        elif self.alliesPower > self.enemiesPower:
            self.winning = "Enemy"
        else:
            self.winning = "Tie"

class onRevealActivatesTwice(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Double on reveals"
        self.on_reveal_number_base = self.on_reveal_number_base * 2

class Limbo(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Limbo"
    def onRevealLocation(self):
        self.status["maxturns"] = 7
    def changeLocation(self, newLocation):
        super().changeLocation(newLocation)
        check = False
        map_keys = map(self.locationlist.get, self.locationlist)
        for key in map_keys:
            if key.name == "Limbo":
                check = True
        if not check:
            self.status["maxturns"] = 6

class OnslaughtCitadel(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Onslaught Citadel"
        self.description = "Ongoing effects here are doubled"
        self.ongoing_number_base = 2

class Asgard(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Asgard"
        self.description = "After turn 4, whoever is winning here draws 2 cards"
    
    def endOfTurn(self):
        super().endOfTurn()
        if self.status["turncounter"] == 4:
            if self.winning == "Ally":
                print("Allies drawing 2")
                for i in range(2):
                    if self.status["allydeck"] != []:
                        self.status["allyhand"].append(self.status["allydeck"].pop())
            elif self.winning == "Enemy":
                print("Enemies drawing 2")
                for i in range(2):
                    if self.status["enemydeck"] != []:
                        self.status["enemyhand"].append(self.status["enemydeck"].pop())
    
class CastleBlackstone(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Castle Blackstone"
        self.description = "The player winning here gets +1 energy each turn"
    
    def startOfTurn(self):
        super().startOfTurn()
        if self.winning == "Ally":
            self.status["tempenergyally"] += 1
        elif self.winning == "Enemy":
            self.status["tempenergyenemy"] += 1