from Locations import Location

class Sewersystem(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Sewer System"
        self.description = "Cards here have -1 Power"
    
    def applyOngoing(self, location):
        for unit in self.allies + self.enemies:
            unit.ongoing_to_apply.append(self)
    
    def ongoing(self, unit):
        unit.ongoing_buff -= 1