from Locations import Location

class PlunderCastle(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Plunder Castle"
        self.description = "Only cards that cost 6 can be played here"
    
    def canCardBePlayed(self,unit):
        if unit.cur_cost == 6 and unit.can_be_played:
            return True
        else: 
            return False
        