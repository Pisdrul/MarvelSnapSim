from Locations import Location

class CrimsonCosmos(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Crimson Cosmos"
        self.description = "Cards that cost 1,2 or 3 can't be played here"
    
    def canCardBePlayed(self,unit):
        if unit.cur_cost == 1 or unit.cur_cost == 2 or unit.cur_cost == 3:
            return False
        elif unit.can_be_played:
            return True
        else:
            return False
