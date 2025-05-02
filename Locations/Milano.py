from Locations import Location

class Milano(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Milano"
        self.description = "Turn 5 is the only turn cards can be played here"
    
    def canCardBePlayed(self,unit):
        if self.status["turncounter"] == 5 and unit.can_be_played:
            return True
        else:
            return False