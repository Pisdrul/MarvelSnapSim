from cards import Card

class Heimdall(Card):
    def __init__(self, ally, status):
        super().__init__(6, 10, "Heimdall", ally, status)
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
