from Locations import Location

class CrownCity(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Crown City"
        self.description = "Whoever is winning here gets +4 Power to adjacent locations"
    
    def applyOngoing(self, location):
        try:
            self.returnRightOrLeftLocation(1).ongoing_to_apply.append(self)
        except:
            pass
        try:
            self.returnRightOrLeftLocation(-1).ongoing_to_apply.append(self)
        except:
            pass
    
    def ongoing(self, location):
        if self.winning == "Ally":
            location.allies_power_buff_sum += 4
        elif self.winning == "Enemy":
            location.enemies_power_buff_sum += 4