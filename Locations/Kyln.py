from Locations import Location

class Kyln(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Kyln"
        self.description = "You can't play cards here after turn 4."
    
    def canCardBePlayed(self,unit):
        if self.status["turncounter"] <= 4 and unit.can_be_played:
            return True
        else:
            return False