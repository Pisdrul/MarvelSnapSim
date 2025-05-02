from Locations import Location 

class Hellfireclub(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Hellfire Club"
        self.description = "You can't play 1 cost cards here"
    
    def canCardBePlayed(self,unit):
        if unit.cur_cost == 1:
            return False
        elif unit.can_be_played:
            return True
        else:
            return False
