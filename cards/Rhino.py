from cards import Card
from Locations import Location

class Rhino(Card):
    def __init__(self, ally, status):
        super().__init__(3, 3, "Rhino", ally, status)
        self.description = "On Reveal: Ruin this location. (Remove its ability)"
    
    class Ruin(Location):
        def __init__(self, number, status, locationlist):
            super().__init__(number, status, locationlist)
            self.name = "Ruin"
            self.description = "No ability"
    
    def onReveal(self, locationlist):
        self.location.changeLocation(self.Ruin(self.location.locationNum, self.status, locationlist))