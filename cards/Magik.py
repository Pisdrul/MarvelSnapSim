from cards import Card
from Locations import Limbo
class Magik(Card):
    def __init__(self, ally, status):
        super().__init__(3, 2, "Magik", ally, status)
        self.description = "On Reveal: Change this location to Limbo (doesnt work after turn 5)"
    
    def onReveal(self,locationlist):
        if self.status["turncounter"] <=5:
            newloc = Limbo(0,self.status, locationlist)
            self.location.changeLocation(newloc)

        else:
            print("doesnt work after turn 5!")