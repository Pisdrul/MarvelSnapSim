from Locations import Location

class Necrosha(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Necrosha"
        self.description = "Cards here have -2 Power"
    
    def applyOngoing(self, location):
        for unit in self.allies + self.enemies:
            unit.ongoing_to_apply.append(self)
    
    def ongoing(self, unit):
        unit.ongoing_buff -= 2