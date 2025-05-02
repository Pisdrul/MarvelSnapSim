from Locations import Location

class Nidavellir(Location):
    def __init__(self, number, status, locationlist):
        super().__init__(number, status, locationlist)
        self.name = "Nidavellir"
        self.description = "Cards here have +5 Power"
    
    def applyOngoing(self, location):
        for unit in self.allies + self.enemies:
            unit.ongoing_to_apply.append(self)
    
    def ongoing(self, unit):
        unit.ongoing_buff += 5