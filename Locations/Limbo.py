from Locations import Location 

class Limbo(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Limbo"
        self.description = "There is a turn 7 this game."
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
