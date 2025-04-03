from Locations.Location import Location
import random
import copy

class Wakanda(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Wakanda"
        self.description = "Cards here can't be destroyed"
        self.can_destroy = False

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
        self.on_reveal_num = self.on_reveal_number * 2

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